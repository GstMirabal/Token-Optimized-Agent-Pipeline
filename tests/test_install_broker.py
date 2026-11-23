"""Tests for scripts/install_broker.py (Sprint 060 unit A-04, ADR-0025 D5)."""

from __future__ import annotations

import importlib
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"

pytestmark = pytest.mark.skipif(
    shutil.which("git") is None or shutil.which("ssh-keygen") is None,
    reason="git and ssh-keygen are required",
)

SRC = "scripts/github_broker.py"


def _git(root: Path, *args: str) -> str:
    done = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True, check=True
    )
    return done.stdout.strip()


def _keygen(path: Path) -> str:
    subprocess.run(
        ["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(path)], check=True
    )
    return path.with_suffix(".pub").read_text().strip()


@pytest.fixture()
def mod(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    monkeypatch.syspath_prepend(str(SCRIPTS))
    sys.modules.pop("install_broker", None)
    monkeypatch.setenv("AGENTS_BROKER_HOME", str(tmp_path / "home"))
    return importlib.import_module("install_broker")


@pytest.fixture()
def repo(tmp_path: Path) -> dict:
    root = tmp_path / "repo"
    (root / "scripts").mkdir(parents=True)
    (root / "config").mkdir()
    keys = tmp_path / "k"
    keys.mkdir()
    pub = _keygen(keys / "good")
    other_pub = _keygen(keys / "other")
    del other_pub
    (root / "config" / "allowed_signers").write_text(
        f'agents-broker namespaces="git" {pub}\n'
    )
    (root / SRC).write_text("print('tagged')\n")
    _git(root, "init", "-q", "-b", "main")
    for key, value in (
        ("user.email", "t@example.invalid"),
        ("user.name", "t"),
        ("commit.gpgsign", "false"),
        ("tag.gpgsign", "false"),
        ("gpg.format", "ssh"),
    ):
        _git(root, "config", key, value)
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "init")
    return {"root": root, "keys": keys, "head": _git(root, "rev-parse", "HEAD")}


def _sign_tag(repo: dict, tag: str, key: str) -> None:
    root = repo["root"]
    _git(root, "config", "user.signingkey", str(repo["keys"] / key))
    _git(root, "tag", "-s", "-m", "release", tag)


def _installed(tmp_path: Path) -> Path:
    return tmp_path / "home" / "github_broker.py"


def test_signed_tag_installs_git_show_content(mod, repo, tmp_path) -> None:
    _sign_tag(repo, "v1.0.0", "good")
    assert mod.main(["--tag", "v1.0.0"], root=repo["root"]) == 0
    assert _installed(tmp_path).read_bytes() == b"print('tagged')\n"


def test_modified_working_tree_is_not_installed(mod, repo, tmp_path) -> None:
    _sign_tag(repo, "v1.0.0", "good")
    (repo["root"] / SRC).write_text("print('evil')\n")
    assert mod.main(["--tag", "v1.0.0"], root=repo["root"]) == 0
    assert _installed(tmp_path).read_bytes() == b"print('tagged')\n"


def test_unsigned_tag_refused(mod, repo, tmp_path) -> None:
    _git(repo["root"], "tag", "-a", "-m", "x", "v1.0.0")
    assert mod.main(["--tag", "v1.0.0"], root=repo["root"]) == 2
    assert not _installed(tmp_path).exists()


def test_tag_signed_by_unlisted_key_refused(mod, repo, tmp_path) -> None:
    _sign_tag(repo, "v1.0.0", "other")
    assert mod.main(["--tag", "v1.0.0"], root=repo["root"]) == 2
    assert not _installed(tmp_path).exists()


def test_missing_signers_file_refused(mod, repo, tmp_path) -> None:
    _sign_tag(repo, "v1.0.0", "good")
    (repo["root"] / "config" / "allowed_signers").unlink()
    assert mod.main(["--tag", "v1.0.0"], root=repo["root"]) == 2
    assert not _installed(tmp_path).exists()


@pytest.mark.parametrize("tag", ["1.0.0", "v1.0", "v1.0.0-rc1", "--force", "v1.0.0/x"])
def test_malformed_tag_refused(mod, repo, tmp_path, tag) -> None:
    assert mod.main(["--tag", tag], root=repo["root"]) == 2
    assert not _installed(tmp_path).exists()


def test_commit_on_main_installs(mod, repo, tmp_path) -> None:
    assert mod.main(["--commit", repo["head"]], root=repo["root"]) == 0
    assert _installed(tmp_path).read_bytes() == b"print('tagged')\n"


def test_commit_not_on_main_refused(mod, repo, tmp_path) -> None:
    root = repo["root"]
    _git(root, "checkout", "-q", "-b", "side")
    (root / SRC).write_text("print('side')\n")
    _git(root, "commit", "-q", "-am", "side")
    side = _git(root, "rev-parse", "HEAD")
    assert mod.main(["--commit", side], root=root) == 2
    assert not _installed(tmp_path).exists()


def test_short_sha_refused(mod, repo, tmp_path) -> None:
    assert mod.main(["--commit", repo["head"][:12]], root=repo["root"]) == 2
    assert not _installed(tmp_path).exists()


def test_neither_or_both_flags_refused(mod, repo, tmp_path) -> None:
    assert mod.main([], root=repo["root"]) == 2
    both = ["--tag", "v1.0.0", "--commit", repo["head"]]
    assert mod.main(both, root=repo["root"]) == 2
    assert not _installed(tmp_path).exists()


def test_existing_keys_and_config_untouched(mod, repo, tmp_path) -> None:
    keys = tmp_path / "home" / "keys"
    keys.mkdir(parents=True)
    (keys / "app.pem").write_text("secret")
    (tmp_path / "home" / "config.json").write_text("{}")
    assert mod.main(["--commit", repo["head"]], root=repo["root"]) == 0
    assert (keys / "app.pem").read_text() == "secret"
    assert (tmp_path / "home" / "config.json").read_text() == "{}"
    assert sorted(p.name for p in (tmp_path / "home").iterdir()) == [
        "config.json", "github_broker.py", "keys",
    ]


def test_installed_file_mode_is_private(mod, repo, tmp_path) -> None:
    assert mod.main(["--commit", repo["head"]], root=repo["root"]) == 0
    assert _installed(tmp_path).stat().st_mode & 0o077 == 0
