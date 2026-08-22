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


# --- F1/F2: the host-shaped negative corpus --------------------------------
#
# The first version of this unit measured its false-positive rate against this
# repository's 455 tracked files and reported zero. The number was true and
# non-probative: only six tracked files are reachable by the YAML form and no
# tracked file is a Dockerfile at all, so the corpus could not falsify the
# claim. These are stock lines from Kubernetes, Helm, Compose, Terraform and
# CI manifests — the content a host commits — and sixteen of them were flagged
# before the reference-name filter existed.

@pytest.mark.parametrize("filename,line", [
    # A key that names a Secret object, not one that holds a secret.
    ("ingress.yaml",        "    secretName: myapp-tls-certificate\n"),
    ("values.yaml",         "existingSecret: postgresql-credentials\n"),
    ("values.yaml",         "existingSecretPasswordKey: postgres-password\n"),
    ("values.yaml",         "credentialsSecretName: aws-s3-credentials\n"),
    ("values.yaml",         "masterKeySecretName: meilisearch-master-key\n"),
    # The RECOMMENDED secure pattern: a path to a mounted secret.
    ("docker-compose.yml",  "      POSTGRES_PASSWORD_FILE: /run/secrets/db_password\n"),
    ("values.yaml",         "  vault_password_file: /etc/ansible/vault-pass\n"),
    ("values.yaml",         "  private_key_path: /etc/ssl/private/server.pem\n"),
    ("values.yaml",         "  secret_key_file: /var/run/secrets/app.key\n"),
    # Public metadata that merely mentions a credential.
    ("values.yaml",         "  SIGNING_KEY_ID: 4a7c9e2b-1f83-4d56-9a0e-7c3b8f1d2e64\n"),
    ("values.yaml",         "  passwordPolicy: strict-minimum-fourteen\n"),
    (".gitlab-ci.yml",      "  SECRET_DETECTION_EXCLUDED_PATHS: docs/,fixtures/\n"),
    ("values.yaml",         "  api_key_url: https://vault.internal/v1/secret\n"),
    # A URL query parameter that is not a credential.
    ("README.md",           "See https://site.io/search?keywords=machine-learning-2024\n"),
    ("README.md",           "See https://site.io/docs?tokenizer=wordpiece-uncased\n"),
    ("README.md",           "See https://api.io/v1/items?sort_key=created_at_desc\n"),
    ("README.md",           "See https://site.io/?utm_token=newsletter-spring-2026\n"),
    ("README.md",           "See https://site.io/?passwordless=true-for-all-users\n"),
    ("README.md",           "See https://shop.io/p?monkey=plush-toy-large\n"),
    ("Dockerfile",          "ENV API_KEY_FILE /run/secrets/api_key\n"),
    # Named for what it points AT, not what it points with, so the name-side
    # test structurally cannot see it. The canonical Google Cloud variable.
    ("docker-compose.yml",
     "      GOOGLE_APPLICATION_CREDENTIALS: /run/secrets/gcp-sa.json\n"),
    ("Dockerfile",
     "ENV PYTHONUNBUFFERED=1 GOOGLE_APPLICATION_CREDENTIALS=/app/config/sa.json\n"),
    ("values.yaml",         "  privateKey: /etc/ssl/private/tls.key\n"),
    ("values.yaml",         "  azure_credentials: /etc/azure/credentials.json\n"),
    ("values.yaml",         "  vault_secret: /secret/data/production/app\n"),
])
def test_host_manifests_are_not_flagged(filename, line):
    assert on_commit.find_hardcoded_secret(line, Path(filename)) is None


# The filter above narrows what counts as a leak, so each narrowing needs a
# case proving it did not switch the gate off.
@pytest.mark.parametrize("filename,line,expected", [
    ("values.yaml",        f"  api_key: {LIVE}\n",                    "api_key"),
    ("docker-compose.yml", f"      POSTGRES_PASSWORD: {LIVE}\n",      "POSTGRES_PASSWORD"),
    ("README.md",          f"curl https://api.io/v1?api_key={LIVE}\n", "api_key"),
    ("Dockerfile",         f"ENV APP_HOME=/srv API_KEY={LIVE}\n",     "API_KEY"),
    ("api.Dockerfile",     f"ENV AUTH_TOKEN={LIVE}\n",                "AUTH_TOKEN"),
    ("config.yml.example", f"api_key: {LIVE}\n",                      "api_key"),
    ("values.YAML",        f"secret_key: {LIVE}\n",                   "secret_key"),
])
def test_real_leaks_survive_the_narrowing(filename, line, expected):
    assert on_commit.find_hardcoded_secret(line, Path(filename)) == expected


def test_pem_private_key_in_a_block_scalar_is_caught():
    """A block scalar's value token is one character, so the key line alone
    can never carry the evidence. The PEM body is matched instead."""
    content = (
        "private_key: |\n"
        "  -----BEGIN RSA PRIVATE KEY-----\n"
        "  MIIEowIBAAKCAQEA7f2a4c8e1b7d3a56\n"
    )
    found = on_commit.find_hardcoded_secret(content, Path("values.yaml"))
    assert found == "PRIVATE KEY"


# The PEM form was first written to return before the exclusion filters, which
# made it the one form an author could not write a legitimate example against.
# It blocked a setup guide whose body was `YOUR_PRIVATE_KEY_HERE` — a phrase
# already in PLACEHOLDER_MARKERS.
@pytest.mark.parametrize("content", [
    "-----BEGIN RSA PRIVATE KEY-----\nYOUR_PRIVATE_KEY_HERE\n-----END RSA PRIVATE KEY-----\n",
    "-----BEGIN PRIVATE KEY-----\nchangeme\n-----END PRIVATE KEY-----\n",
    "-----BEGIN PRIVATE KEY-----\nEXAMPLE-PLACEHOLDER-NOT-A-REAL-KEY\n-----END PRIVATE KEY-----\n",
    "Files beginning with `-----BEGIN PRIVATE KEY-----` are PKCS#8 keys.\n",
])
def test_documented_pem_examples_are_not_flagged(content):
    assert on_commit.find_hardcoded_secret(content, Path("docs/TLS_SETUP.md")) is None


# A URL is a pointer only when the key says so. When the URL IS the credential
# — a capability URL, a DSN with inline userinfo — exempting it lost detections
# this gate made before C3 existed, while the auditor half went on calling a
# Slack webhook a secret.
@pytest.mark.parametrize("filename,line,expected", [
    ("config/slack.py",
     ('SLACK_WEBHOOK_SECRET = "https://hooks.slack.com/services/TABCDEFGH/'
      'BABCDEFGH/abcdefghij1234567890abcd"\n'),
     "SLACK_WEBHOOK_SECRET"),
    ("config/db.py",
     'MONGO_PASSWORD = "mongodb+srv://admin:Tr0ub4dor3@cluster0.mongodb.net"\n',
     "MONGO_PASSWORD"),
    ("deploy/amqp.yaml",
     "amqp_password: amqp://user:R3allySecret@rabbit:5672/\n",
     "amqp_password"),
])
def test_a_credential_that_is_a_url_is_still_a_credential(filename, line, expected):
    assert on_commit.find_hardcoded_secret(line, Path(filename)) == expected


def test_a_key_that_points_at_a_url_is_still_a_pointer():
    """The name side, not the value side, is what makes this one clean."""
    line = "  api_key_url: https://vault.internal/v1/secret\n"
    assert on_commit.find_hardcoded_secret(line, Path("values.yaml")) is None


def test_compose_secrets_list_is_not_a_credential():
    """`secrets: [db_password]` names which secrets a service consumes."""
    content = "services:\n  db:\n    secrets: [db_password]\n"
    assert on_commit.find_hardcoded_secret(content, Path("docker-compose.yml")) is None


# --- secret_forms_for: the selector itself ----------------------------------

@pytest.mark.parametrize("filename,expected", [
    ("values.yaml",        {"SECRET_ASSIGNMENT", "QUERY_STRING_SECRET", "PRIVATE_KEY_BLOCK", "YAML_SECRET"}),
    ("values.YAML",        {"SECRET_ASSIGNMENT", "QUERY_STRING_SECRET", "PRIVATE_KEY_BLOCK", "YAML_SECRET"}),
    ("config.yml.example", {"SECRET_ASSIGNMENT", "QUERY_STRING_SECRET", "PRIVATE_KEY_BLOCK", "YAML_SECRET"}),
    ("Dockerfile",         {"SECRET_ASSIGNMENT", "QUERY_STRING_SECRET", "PRIVATE_KEY_BLOCK", "DOCKERFILE_SECRET"}),
    ("Dockerfile.prod",    {"SECRET_ASSIGNMENT", "QUERY_STRING_SECRET", "PRIVATE_KEY_BLOCK", "DOCKERFILE_SECRET"}),
    ("api.Dockerfile",     {"SECRET_ASSIGNMENT", "QUERY_STRING_SECRET", "PRIVATE_KEY_BLOCK", "DOCKERFILE_SECRET"}),
    ("settings.py",        {"SECRET_ASSIGNMENT", "QUERY_STRING_SECRET", "PRIVATE_KEY_BLOCK"}),
    ("Makefile",           {"SECRET_ASSIGNMENT", "QUERY_STRING_SECRET", "PRIVATE_KEY_BLOCK"}),
])
def test_secret_forms_for_selects_by_format(filename, expected):
    by_pattern = {
        id(on_commit.SECRET_ASSIGNMENT): "SECRET_ASSIGNMENT",
        id(on_commit.QUERY_STRING_SECRET): "QUERY_STRING_SECRET",
        id(on_commit.PRIVATE_KEY_BLOCK): "PRIVATE_KEY_BLOCK",
        id(on_commit.YAML_SECRET): "YAML_SECRET",
        id(on_commit.DOCKERFILE_SECRET): "DOCKERFILE_SECRET",
    }
    selected = {by_pattern[id(f)] for f in on_commit.secret_forms_for(Path(filename))}
    assert selected == expected


def test_secret_forms_for_without_a_path_takes_the_safe_subset():
    selected = on_commit.secret_forms_for(None)
    assert on_commit.YAML_SECRET not in selected
    assert on_commit.DOCKERFILE_SECRET not in selected


# --- audit_secret_shielding: the integration layer --------------------------
#
# Every other secret test calls find_hardcoded_secret directly, so the layer
# that resolves the path, applies the test-artifact skip and runs the
# forbidden-extension branch had no coverage at all — named by the Tester gate.

def _repo_with_staged(tmp_path, files: dict) -> Path:
    """Builds a throwaway git repository with `files` staged."""
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    for name, body in files.items():
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body, encoding="utf-8")
        subprocess.run(["git", "add", "-f", name], cwd=tmp_path, check=True)
    return tmp_path


def test_audit_blocks_a_leak_in_a_staged_manifest(tmp_path, monkeypatch):
    _repo_with_staged(tmp_path, {"charts/values.yaml": f"api_key: {LIVE}\n"})
    monkeypatch.chdir(tmp_path)
    assert not on_commit.audit_secret_shielding()


def test_audit_allows_a_stock_manifest(tmp_path, monkeypatch):
    _repo_with_staged(tmp_path, {
        "deploy/ingress.yaml": "spec:\n  tls:\n    - secretName: myapp-tls-cert\n",
        "docker-compose.yml": "services:\n  db:\n    secrets: [db_password]\n",
    })
    monkeypatch.chdir(tmp_path)
    assert on_commit.audit_secret_shielding()


def test_audit_skips_test_artifacts(tmp_path, monkeypatch):
    _repo_with_staged(tmp_path, {"tests/fixtures.yaml": f"api_key: {LIVE}\n"})
    monkeypatch.chdir(tmp_path)
    assert on_commit.audit_secret_shielding()


def test_audit_blocks_a_forbidden_extension(tmp_path, monkeypatch):
    _repo_with_staged(tmp_path, {"deploy/server.pem": "not a real key\n"})
    monkeypatch.chdir(tmp_path)
    assert not on_commit.audit_secret_shielding()


def test_a_path_exemption_does_not_reach_a_bare_credential():
    """The path test must not become the next over-wide exemption.

    A credential is not a path, and a value-side test that let one through
    would repeat the `://` mistake in the other direction.
    """
    line = "  GOOGLE_APPLICATION_CREDENTIALS: 9f2a4c8e1b7d3a5690b4e2c1f8a7d6e3\n"
    found = on_commit.find_hardcoded_secret(line, Path("docker-compose.yml"))
    assert found == "GOOGLE_APPLICATION_CREDENTIALS"


# --- C3.2: the suppression affordance ---------------------------------------
#
# Value shape cannot separate a pointer from a credential — three rules over
# three gate rounds each narrowed the last and each was wrong in a new
# direction. A gate with no way to comply is a gate that gets disabled, so the
# residual shapes get a declared waiver instead of a fourth narrowing.

@pytest.mark.parametrize("filename,line", [
    # Confirmed stock: `gcloud auth application-default login` writes the
    # second of these, and mounting ~/.config/gcloud is documented practice.
    ("docker-compose.yml",
     "      GOOGLE_APPLICATION_CREDENTIALS: ./secrets/gcp-sa.json\n"),
    ("docker-compose.yml",
     ("      GOOGLE_APPLICATION_CREDENTIALS: ~/.config/gcloud/"
      "application_default_credentials.json\n")),
    ("docker-compose.yml",
     "      GOOGLE_APPLICATION_CREDENTIALS: ../shared/sa-key.json\n"),
    ("docker-compose.yml",
     "      GOOGLE_APPLICATION_CREDENTIALS: /sa-key.json\n"),
])
def test_relative_and_single_segment_pointers_are_clean(filename, line):
    assert on_commit.find_hardcoded_secret(line, Path(filename)) is None


@pytest.mark.parametrize("line", [
    "  azure_credentials: /etc/azure-creds  # secret-scan: allow no extension, mounted dir\n",
    "  vault_secret: /secret/data/prod/  # secret-scan: allow trailing slash, KV mount\n",
    "  private_key: /var/my+app/tls.key  # secret-scan: allow plus sign in vendor path\n",
])
def test_a_declared_waiver_suppresses_the_finding(line):
    assert on_commit.find_hardcoded_secret(line, Path("values.yaml")) is None


@pytest.mark.parametrize("line", [
    # No reason given: the marker is an audit trail, not an off switch.
    "  api_key: 9f2a4c8e1b7d3a5690b4e2c1f8a7d6e3  # secret-scan: allow\n",
    "  api_key: 9f2a4c8e1b7d3a5690b4e2c1f8a7d6e3  # secret-scan:allow   \n",
    # A waiver on a different line does not reach this one.
    ("  other: x  # secret-scan: allow unrelated\n"
     "  api_key: 9f2a4c8e1b7d3a5690b4e2c1f8a7d6e3\n"),
])
def test_a_waiver_without_a_reason_or_on_another_line_does_not_suppress(line):
    assert on_commit.find_hardcoded_secret(line, Path("values.yaml")) is not None


def test_a_waiver_is_announced_at_commit_time(tmp_path, monkeypatch, capsys):
    """A silent bypass is how RA-09 gets defeated by its own control."""
    _repo_with_staged(tmp_path, {
        "values.yaml":
            "  azure_credentials: /etc/azure-creds"
            "  # secret-scan: allow no extension, mounted dir\n",
    })
    monkeypatch.chdir(tmp_path)
    assert on_commit.audit_secret_shielding()
    assert "Secret scan waived" in capsys.readouterr().out


def test_a_pem_body_is_never_treated_as_a_path():
    """The path test can only cost detection on the PEM form."""
    content = (
        "-----BEGIN RSA PRIVATE KEY-----\n"
        "/fgwTBxuAVPH1A17UzI/Fk3sXUsYwMHj/PNvuXKIJLzsPnGa4Y5sewHI9btQi1Ea\n"
    )
    assert on_commit.find_hardcoded_secret(content, Path("id_rsa")) == "PRIVATE KEY"
