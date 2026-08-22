"""Tests for hooks/on_commit.py — the PreToolUse gate that can block real
commits/pushes. Covers the RA-12 push guard, commit message validation, the
Three-File Skill Standard audit, and the hardcoded-secret scan (F-086-S2)."""
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from hooks import on_commit


# --- RA-12 push guard -------------------------------------------------------

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


def test_extract_commit_message_heredoc():
    # The `-m "$(cat <<'EOF' ... EOF)"` idiom used for multi-line commit
    # bodies: this hook sees the raw, unresolved bash command text, so the
    # naive quoted-string branch alone would mis-extract everything up to
    # the first embedded '"' instead of the heredoc's real content.
    command = (
        "git commit -m \"$(cat <<'EOF'\n"
        "feat(x): multi-line message #01\n"
        "\n"
        "Body line explaining the change.\n"
        "EOF\n"
        ")\""
    )
    message = on_commit.extract_commit_message(command)
    assert message == (
        "feat(x): multi-line message #01\n\nBody line explaining the change."
    )
    assert on_commit.is_valid_commit_message(message)

    # A heredoc body that genuinely isn't a valid Conventional Commit must
    # still be rejected — the fix must not open a validation bypass.
    bad_command = (
        "git commit -m \"$(cat <<'EOF'\n"
        "not conventional and missing a sprint id\n"
        "EOF\n"
        ")\""
    )
    bad_message = on_commit.extract_commit_message(bad_command)
    assert not on_commit.is_valid_commit_message(bad_message)


# --- Three-File Skill Standard audit ---------------------------------------

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
    return on_commit.audit_three_file_standard()


def test_knowledge_skill_needs_only_frontmatter(tmp_path, monkeypatch):
    _make_skill(tmp_path, "guide-skill")
    assert _audit_in(tmp_path, monkeypatch, ["skills/guide-skill/SKILL.md"])


def test_knowledge_skill_without_frontmatter_fails(tmp_path, monkeypatch):
    _make_skill(tmp_path, "bad-skill", frontmatter=False)
    assert not _audit_in(tmp_path, monkeypatch, ["skills/bad-skill/SKILL.md"])


def test_executable_skill_requires_full_standard(tmp_path, monkeypatch):
    _make_skill(tmp_path, "tool-skill", scripts=True)  # no README, no __init__
    assert not _audit_in(tmp_path, monkeypatch, ["skills/tool-skill/scripts/run.py"])


def test_executable_skill_full_standard_passes(tmp_path, monkeypatch):
    _make_skill(tmp_path, "tool-skill", scripts=True, readme=True, init=True)
    assert _audit_in(tmp_path, monkeypatch, ["skills/tool-skill/scripts/run.py"])


# --- F-086-S2: the secret pattern reads three more forms --------------------
#
# The list of scanned files was good and the pattern was narrow: it required a
# Python/JS assignment to a QUOTED literal, so a Dockerfile `ENV`, a YAML
# `key: value` and a credential in a URL query string all read as clean. Every
# detection case below was measured failing against the parent of this commit.

LIVE = "sk-live-9f2a4c8e1b7d3a56"


@pytest.mark.parametrize("filename,content,expected_name", [
    ("Dockerfile",         f"ENV API_KEY={LIVE}\n",                       "API_KEY"),
    ("Dockerfile",         f"ENV API_KEY {LIVE}\n",                       "API_KEY"),
    ("Dockerfile.prod",    f"ARG AUTH_TOKEN={LIVE}\n",                    "AUTH_TOKEN"),
    ("Dockerfile",         f'ENV SECRET_KEY="{LIVE}"\n',                  "SECRET_KEY"),
    ("docker-compose.yml", f"api_key: {LIVE}\n",                          "api_key"),
    ("values.yaml",        f'secret_key: "{LIVE}"\n',                     "secret_key"),
    ("values.yaml",        f"  - private_key: {LIVE}\n",                  "private_key"),
    ("client.py",          f'url = "https://x.io/v1?api_key={LIVE}"\n',   "api_key"),
    ("README.md",          f'"https://x.io/?a=1&access_token={LIVE}"\n',  "access_token"),
    ("settings.py",        f'SECRET_KEY = "{LIVE}"\n',                    "SECRET_KEY"),
])
def test_secret_forms_are_detected(filename, content, expected_name):
    found = on_commit.find_hardcoded_secret(content, Path(filename))
    assert found == expected_name


# The exclusions are what keep this gate usable: it already blocked a real host
# once on a false positive. Every one of them must survive the three new forms.
@pytest.mark.parametrize("filename,content", [
    ("views.py",           'password = request.data.get("password")\n'),
    ("settings.py",        'EMAIL_HOST_PASSWORD = config["EMAIL_HOST_PASSWORD"]\n'),
    ("settings.py",        'API_KEY = "${OPENAI_API_KEY}"\n'),
    ("settings.py",        'API_KEY = "$OPENAI_API_KEY"\n'),
    ("settings.py",        'API_KEY = "your-api-key-here"\n'),
    ("settings.py",        'API_KEY = "abc"\n'),
    ("values.yaml",        "api_key: ${VAULT_API_KEY}\n"),
    ("values.yaml",        "api_key: changeme\n"),
    ("models.py",          "password: str = None\n"),
    ("models.py",          "password: str\n"),
    ("Dockerfile",         "ENV API_KEY=${BUILD_API_KEY}\n"),
    ("Dockerfile",         "ENV API_KEY=changeme\n"),
    ("client.py",          'url = "https://x.io/v1?api_key=${TOKEN}"\n'),
    ("client.py",          'url = "https://x.io/v1?api_key=your-key"\n'),
])
def test_non_leaks_are_not_flagged(filename, content):
    assert on_commit.find_hardcoded_secret(content, Path(filename)) is None


# A mapping form is only a mapping in a file that uses mappings. These four
# lines are real content from this repository's own skill documentation, and
# all four were flagged when the YAML form ran against every staged file — the
# false-positive class this gate has already blocked a host over.
@pytest.mark.parametrize("content", [
    "  password: hashedPassword,\n",
    "  password: z.string().min(8),\n",
    "  password: process.env.DB_PASSWORD,\n",
    "      POSTGRES_PASSWORD: postgres\n",
])
def test_mapping_form_does_not_run_against_markdown(content):
    assert on_commit.find_hardcoded_secret(content, Path("SKILL.md")) is None


def test_mapping_form_still_runs_against_real_yaml():
    """The gate above must narrow where YAML_SECRET applies, not disable it."""
    content = "      POSTGRES_PASSWORD: 8Kd2mQx7Rt\n"
    assert on_commit.find_hardcoded_secret(
        content, Path("docker-compose.yml")) == "POSTGRES_PASSWORD"


def test_unknown_path_uses_only_format_agnostic_forms():
    """A caller with no path gets the safe subset, not the widest one."""
    assert on_commit.find_hardcoded_secret(f"api_key: {LIVE}\n") is None
    assert on_commit.find_hardcoded_secret(f'K = "{LIVE}"\n') is None
    assert on_commit.find_hardcoded_secret(
        f'SECRET_KEY = "{LIVE}"\n') == "SECRET_KEY"
