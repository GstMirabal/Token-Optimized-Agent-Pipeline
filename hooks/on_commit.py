import subprocess
import sys
import itertools
import json
import re
from datetime import datetime
from pathlib import Path

import sys
# Add parent directory to path so 'hooks' module can be found if run directly
sys.path.append(str(Path(__file__).parent.parent))
from hooks.telemetry import log_error

def get_staged_files() -> list[str]:
    """Retrieves the list of files staged for the current commit."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        print(f"⚠️ [DEVOPS AGENT] Git error: {e}")
        return []

def audit_three_file_standard() -> bool:
    """Certifies the Three-File Skill Standard (agents.md §3 three_file_standard) for modified skills."""
    staged_files = get_staged_files()
    if not staged_files:
        return True

    # Identify skills that have modified files
    modified_skills = set()
    for file_path in staged_files:
        path = Path(file_path)
        if "skills/" in file_path:
            # skills/skill-name/... -> skill-name is at index 1 (flat topology)
            parts = path.parts
            if len(parts) >= 2 and parts[0] == "skills":
                skill_root = Path(*parts[:2])
                modified_skills.add(skill_root)

    violations = []
    for skill_path in modified_skills:
        print(f"🔍 [DEVOPS AGENT] Auditing {skill_path}...")

        skill_md = skill_path / "SKILL.md"
        scripts = skill_path / "scripts"

        # Every skill needs a SKILL.md with name/description frontmatter.
        if not skill_md.exists():
            violations.append(f"{skill_path}: Missing SKILL.md")
        else:
            head = skill_md.read_text(encoding="utf-8")[:500]
            if not head.startswith("---") or "name:" not in head or "description:" not in head:
                violations.append(f"{skill_path}: SKILL.md missing name/description frontmatter")

        # Full standard only applies to executable skills (agents.md §3 three_file_standard):
        # a skill that ships scripts/ must also ship README.md and scripts/__init__.py.
        # Knowledge skills (no scripts/) are complete with just SKILL.md.
        if scripts.is_dir():
            if not (skill_path / "README.md").exists():
                violations.append(f"{skill_path}: Executable skill missing README.md")
            if not (scripts / "__init__.py").exists():
                violations.append(f"{skill_path}: scripts/ missing __init__.py")

    if violations:
        for v in violations:
            print(f"❌ [ON_COMMIT] Structure Violation: {v}")
        return False
    
    return True

# A secret leaks when a secret-named identifier is assigned a STRING LITERAL.
# Matching the bare substring "PASSWORD =" instead flags every legitimate read
# of a secret (`password = request.data.get("password")`,
# `EMAIL_HOST_PASSWORD = config["EMAIL_HOST_PASSWORD"]`), which no project
# handling authentication can avoid — the gate then blocks every commit and
# stops meaning anything. The literal on the right-hand side is what
# distinguishes a leak from a lookup.
SECRET_WORDS = (
    r"API_?KEY|SECRET|PASSWORD|PASSWD|PRIVATE_?KEY|AUTH_?TOKEN"
    r"|MASTER_?KEY|SIGNING_?KEY|ACCESS_?KEY|PEPPER|CREDENTIAL"
)

# The affix groups are `*`, not `+`: the secret word may be the whole
# identifier (MASTER_KEY), a suffix (EMAIL_HOST_PASSWORD) or a prefix
# (SECRET_KEY_FALLBACK).
SECRET_ASSIGNMENT = re.compile(
    rf"""^[ \t]*
        (?P<name>[A-Za-z0-9_]*(?:{SECRET_WORDS})[A-Za-z0-9_]*)
        [ \t]*(?::[^=\n]+)?[ \t]*=[ \t]*
        (?P<q>['"])(?P<value>(?:(?!(?P=q)).)*)(?P=q)
    """,
    re.IGNORECASE | re.MULTILINE | re.VERBOSE,
)

# The quoted-literal assignment above is the Python/JS form and only that form.
# Three others carry credentials just as directly and read as clean against it
# (F-086-S2), so each gets its own alternation rather than one regex widened
# until it matches everything: a Dockerfile `ENV`/`ARG`, a YAML `key: value`,
# and a credential in a URL query string. Every one of them is filtered by the
# same exclusions in find_hardcoded_secret — the gate has already blocked a
# real host once on a false positive, and widening what it reads is exactly
# when that risk returns.

# `ENV API_KEY=x`, `ARG API_KEY=x`, and the legacy space-separated `ENV KEY x`.
DOCKERFILE_SECRET = re.compile(
    rf"""^[ \t]*(?:ENV|ARG)[ \t]+
        (?P<name>[A-Za-z0-9_]*(?:{SECRET_WORDS})[A-Za-z0-9_]*)
        (?:[ \t]*=[ \t]*|[ \t]+)
        (?P<value>"[^"\n]*"|'[^'\n]*'|[^\s#]+)
    """,
    re.IGNORECASE | re.MULTILINE | re.VERBOSE,
)

# YAML `api_key: value`, including a list item (`- api_key: value`). The value
# is a single token deliberately: `password: str = None` is a Python type
# annotation, not a mapping, and a token-bounded value reads `str` there —
# under MIN_SECRET_LENGTH, so it is dropped instead of blocking the commit.
YAML_SECRET = re.compile(
    rf"""^[ \t]*(?:-[ \t]+)?
        (?P<name>[A-Za-z0-9_-]*(?:{SECRET_WORDS})[A-Za-z0-9_-]*)
        [ \t]*:[ \t]+
        (?P<value>"[^"\n]*"|'[^'\n]*'|[^\s#]+)
    """,
    re.IGNORECASE | re.MULTILINE | re.VERBOSE,
)

# `?api_key=…` / `&access_token=…` anywhere in a line: a credential pasted into
# a URL is not an assignment and so was never matched.
QUERY_STRING_SECRET = re.compile(
    r"""[?&](?P<name>\w*(?:key|token|secret|password)\w*)=
        (?P<value>[^&\s'"#]+)
    """,
    re.IGNORECASE | re.VERBOSE,
)

# A mapping form is only a mapping in a file that uses mappings. Applied to
# every staged file regardless of type, YAML_SECRET reads JavaScript object
# literals inside Markdown code blocks as leaks — measured against this
# repository: five false positives across its own skill documentation, among
# them `password: process.env.DB_PASSWORD`, which is the sanctioned RA-09
# pattern. So the format-specific forms are selected by path, and the
# format-agnostic ones always apply.
YAML_SUFFIXES = (".yml", ".yaml")
DOCKERFILE_NAMES = ("Dockerfile", "Containerfile")


def secret_forms_for(path: Path | None) -> tuple:
    """Selects the secret patterns that apply to one file.

    Args:
        path: Path of the file being scanned, or None when it is not known.

    Returns:
        The applicable compiled patterns. A format-specific form is omitted
        when the path does not identify that format, including when the path
        is unknown: a leak missed in an unidentified file is caught by the
        next scan, whereas a gate that blocks a legitimate commit gets
        disabled and then catches nothing at all.
    """
    forms = [SECRET_ASSIGNMENT, QUERY_STRING_SECRET]
    if path is not None and path.suffix.lower() in YAML_SUFFIXES:
        forms.append(YAML_SECRET)
    if path is not None and (
        path.name in DOCKERFILE_NAMES or path.name.startswith("Dockerfile.")
    ):
        forms.append(DOCKERFILE_SECRET)
    return tuple(forms)

# Values that are obviously not live credentials.
PLACEHOLDER_MARKERS = (
    "example", "changeme", "change-me", "placeholder", "your-", "your_",
    "dummy", "sample", "redacted", "xxxx", "insert", "fake", "test",
)

MIN_SECRET_LENGTH = 8


def _is_test_artifact(path: Path) -> bool:
    """Reports whether a path holds test fixtures rather than shipped code.

    Test credentials are deliberately hardcoded and carry no production value,
    so scanning them only produces noise.
    """
    parts = {p.lower() for p in path.parts}
    if {"tests", "test", "fixtures", "factories"} & parts:
        return True
    name = path.name.lower()
    return (
        name.startswith("test_")
        or name.endswith("_test.py")
        or name in {"conftest.py", "factories.py", "tests.py"}
    )


def _unquote(value: str) -> str:
    """Strips one matched pair of surrounding quotes, if present.

    Args:
        value: A captured value, quoted or bare depending on the form matched.

    Returns:
        The value without its surrounding quotes.
    """
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
        return value[1:-1]
    return value


def find_hardcoded_secret(content: str, path: Path | None = None) -> str | None:
    """Returns the identifier of the first hardcoded secret found, if any.

    Args:
        content: Full text of a staged file.
        path: Path of that file, used to select the format-specific patterns.

    Returns:
        The offending variable name, or None when nothing credible is found.
    """
    matches = itertools.chain.from_iterable(
        form.finditer(content) for form in secret_forms_for(path)
    )
    for match in matches:
        value = _unquote(match.group("value"))

        if len(value) < MIN_SECRET_LENGTH:
            continue
        # "$VAR" / "${VAR}" are environment interpolation placeholders, which is
        # exactly the sanctioned pattern in config.toml.example (RA-09).
        if value.startswith("$") or value.startswith("{"):
            continue
        if any(marker in value.lower() for marker in PLACEHOLDER_MARKERS):
            continue

        return match.group("name")

    return None


def audit_secret_shielding() -> bool:
    """Certifies secret shielding (agents.md §3 secret_sovereignty / RA-09)."""
    staged_files = get_staged_files()
    
    forbidden_extensions = [".env", ".pem", ".key"]
    forbidden_names = ["secrets.json", "credentials.json"]
    
    violations = []
    for file_path in staged_files:
        path = Path(file_path)
        
        # Check by filename/extension
        if path.suffix in forbidden_extensions or path.name in forbidden_names:
            violations.append(f"Forbidden file staged: {file_path}")
            continue

        # Basic content scanning for API keys or secrets
        try:
            content = subprocess.run(
                ["git", "show", f":{file_path}"],
                capture_output=True,
                text=True,
                check=True
            ).stdout
            
            if _is_test_artifact(path):
                continue

            leak = find_hardcoded_secret(content, path)
            if leak:
                violations.append(
                    f"Hardcoded secret assigned to '{leak}' in {file_path}"
                )
        except Exception:
            # Skip binary files or git errors
            continue

    if violations:
        for v in violations:
            print(f"❌ [ON_COMMIT] Secret Violation: {v}")
        return False

    return True

DEPLOY_UNLOCK = Path(".agents/.deploy_unlock")

# Conventional Commit type + optional scope + description ending in #[Sprint_ID]
# (agents.md §5 historical_log). Example: "feat(auth): add login flow #078".
COMMIT_MSG_REGEX = re.compile(
    r"^(feat|fix|docs|chore|refactor|test|style|perf|ci|build|revert)"
    r"(\([\w\-./]+\))?!?: .+#\w+"
)


def read_hook_command() -> str:
    """Reads the PreToolUse payload from stdin and returns the Bash command.

    Claude Code invokes PreToolUse hooks on every matching tool call (here: every
    Bash call), passing {"tool_name": ..., "tool_input": {"command": ...}} on stdin.
    Returns "" when there is no payload (e.g. run manually for testing).
    """
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return ""
    return payload.get("tool_input", {}).get("command", "")


def is_blocked_push(command: str) -> bool:
    """RA-12 mechanical enforcement: pushes to main/master are blocked unless the
    deployment workflow has explicitly created the .agents/.deploy_unlock marker."""
    if "git push" not in command:
        return False
    if not re.search(r"git push\s+(?:-[^\s]+\s+)*\S+\s+(main|master)(?=\s|$|:)", command):
        return False
    return not DEPLOY_UNLOCK.exists()


HEREDOC_COMMIT_MSG_REGEX = re.compile(
    r"-m\s+\"\$\(cat\s+<<-?\s*['\"]?(\w+)['\"]?\s*\n(.*?)\n\1\s*\)\"",
    re.DOTALL,
)


def extract_commit_message(command: str) -> str | None:
    """Pulls the -m message out of a git commit command, if present.

    Handles both a plain quoted string and the `-m "$(cat <<'EOF' ...
    EOF)"` heredoc idiom recommended for multi-line Conventional Commit
    bodies: this hook only ever sees the raw, unresolved bash command text
    (Claude Code's PreToolUse payload), never the shell-expanded result, so
    a heredoc's body has to be parsed out of the literal `-m "$(cat <<...`
    syntax explicitly — the naive quoted-string match below stops at the
    first embedded `"` and silently mis-extracts everything before the
    heredoc's actual content, which used to produce false COMMIT_MSG_VIOLATION
    reports for perfectly valid Conventional Commit messages.
    """
    heredoc = HEREDOC_COMMIT_MSG_REGEX.search(command)
    if heredoc:
        return heredoc.group(2)
    m = re.search(r"-m\s+(?:\"([^\"]*)\"|'([^']*)')", command)
    if not m:
        return None
    return m.group(1) if m.group(1) is not None else m.group(2)


def is_valid_commit_message(message: str) -> bool:
    """Conventional Commit + mandatory #[Sprint_ID] suffix (agents.md §5)."""
    first_line = message.splitlines()[0] if message else ""
    return bool(COMMIT_MSG_REGEX.match(first_line))


TEST_PATH = re.compile(r"(^|/)(tests?|__tests__)/|(^|/)test_[^/]+$|_test\.[a-z]+$|\.test\.[a-z]+$")
SOURCE_SUFFIXES = (".py", ".js", ".jsx", ".ts", ".tsx", ".go", ".rs", ".java", ".rb", ".php")
MANIFESTS = ("requirements", "package.json", "pyproject.toml")
# A manifest inside vendored material is not this project's dependency
# declaration. The retroactive run over 156 commits flagged two commits whose
# only "dependency changes" were package.json files under node_modules/ inside
# a vendored `-3rd` skill — nothing the author chose or controls.
VENDORED = ("node_modules/", "-3rd/", "/3rd/", "venv_skillopt/")
DEPENDENCY_LINE = re.compile(r"^Dependency:\s*\S+\s*[—-]\s*\S", re.MULTILINE)


def audit_regression_test(message: str, staged: list[str]) -> str | None:
    """A bug fix must ship the test that proves it (rules/code_craft.md §6).

    `RA-13 SEQUENTIAL_GATES` applied to tests: the failing test is observed
    before the fix, so the change is known to address the cause rather than a
    symptom. Coverage (`qa_and_testing.md §1`) measures quantity; this measures
    ordering, and nothing else did.

    Exempt by design, following the PR #27 lesson that a gate must recognise
    the legitimate case instead of blocking everything that resembles the
    illegitimate one: a `fix(` commit that stages no source file at all has
    nothing to write a test against.

    Args:
        message: The commit message.
        staged: Paths staged for this commit.

    Returns:
        str | None: Failure reason, or None when the commit passes.
    """
    if not message.startswith("fix("):
        return None
    if not any(path.endswith(SOURCE_SUFFIXES) for path in staged):
        return None  # Documentation, workflow or config fix: no test to write.
    if any(TEST_PATH.search(path) for path in staged):
        return None
    return ("A `fix(` commit must stage the test that proves the bug (rules/code_craft.md §6). "
            "Write the failing test, watch it fail, then fix. If this fix genuinely cannot be "
            "tested, that is information about the design — say so and commit as `refactor(` "
            "or `chore(` instead of relabelling it.")


PACKAGE_NAME = re.compile(r'^[+-]\s*"?([A-Za-z0-9_.@/-]+)"?\s*[:=><~^"]')


def newly_added_dependencies(manifests: list[str], ref: str = "--cached") -> set[str]:
    """Package names this diff introduces, ignoring bumps, removals and reorders.

    Firing on any touch of a manifest was the first version of this check, and
    the retroactive run over 156 commits rejected 3 of 3 — including version
    bumps and removals, where demanding a justification line is nonsense. The
    signal is a name that appears on the added side and nowhere on the removed
    side; anything else is maintenance of something already admitted.
    """
    diff = subprocess.run(
        ["git", "diff", ref, "-U0", "--"] + manifests,
        capture_output=True, text=True,
    )
    if diff.returncode != 0:
        return set()

    added, removed = set(), set()
    for line in diff.stdout.splitlines():
        if line.startswith(("+++", "---")):
            continue
        match = PACKAGE_NAME.match(line)
        if not match:
            continue
        (added if line.startswith("+") else removed).add(match.group(1))
    return added - removed


def audit_dependency_justification(message: str, staged: list[str]) -> str | None:
    """A new dependency must say why it earned its place (code_craft.md §7).

    `agents.md §8` governs how a dependency is installed; nothing governed
    whether it should enter. Every dependency is permanent code the project
    does not control.

    Exempt: `chore(deps)`, which is the conventional prefix for version
    maintenance rather than admission of something new.

    Args:
        message: The commit message.
        staged: Paths staged for this commit.

    Returns:
        str | None: Failure reason, or None when the commit passes.
    """
    if message.startswith("chore(deps"):
        return None
    manifests = [path for path in staged
                 if any(m in path for m in MANIFESTS)
                 and not any(v in path for v in VENDORED)]
    if not manifests or not newly_added_dependencies(manifests):
        return None
    if DEPENDENCY_LINE.search(message):
        return None
    return ("This commit adds a dependency without justifying it "
            "(rules/code_craft.md §7). Add a line `Dependency: <name> — <reason>` to the "
            "commit message, or use `chore(deps)` if it is version maintenance rather "
            "than a new dependency.")


def audit_submodule_purity() -> str | None:
    """Refuse a host commit while the framework submodule carries host work.

    `agents.md §3 jurisdiction`. Delegates to `scripts/submodule_purity.py` so
    the rule has one implementation rather than two that can drift apart — the
    close-time gate (`close_workflow.md` Phase 5) invokes the same script.

    Returns:
        str | None: the refusal reason, or None in nucleus mode / when clean.
    """
    script = Path(__file__).resolve().parent.parent / "scripts" / "submodule_purity.py"
    if not script.exists():
        # A missing check is reported by RA-16's invocation coverage, not
        # silently treated as a pass here.
        return None
    result = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
    if result.returncode == 0:
        return None
    return (result.stderr.strip() or
            "Host work found inside the .agents submodule (agents.md §3 jurisdiction).")


def block(reason: str) -> None:
    # Claude Code only feeds stderr back to the model on a blocking hook, and
    # only exit code 2 actually blocks (RA-11 HOOK_BLOCKING_SEMANTICS).
    print(f"❌ [DEVOPS AGENT] {reason}", file=sys.stderr)
    sys.exit(2)


def main():
    command = read_hook_command()

    # Guard 1 (RA-12): no direct pushes to main/master outside deployment.
    if command and is_blocked_push(command):
        log_error("on_commit", "BRANCH_VIOLATION", "Direct push to main/master blocked (RA-12)")
        block("Push to main/master is PROHIBITED (RA-12 Branch Discipline). "
              "Merge through the deployment workflow (/agents:deployment), which creates "
              ".agents/.deploy_unlock for its sanctioned fallback push.")

    # Everything below only applies to git commit invocations.
    if command and "git commit" not in command:
        sys.exit(0)

    # Guard 1.5 (agents.md §3 jurisdiction): a host session's work never lands
    # inside the framework submodule. Checked HERE and not only at close,
    # because by close time the contamination has had a whole sprint to spread
    # and a commit may already record a dirty submodule. No-op in nucleus mode.
    if reason := audit_submodule_purity():
        log_error("on_commit", "JURISDICTION_VIOLATION", reason[:80])
        block(reason)

    # Guard 2 (agents.md §5): Conventional Commit + #[Sprint_ID] suffix.
    # Guards 2-4 need the commit message, which is only reliably available on
    # the agent path (the Bash command carries `-m`). At native pre-commit time
    # git has not yet finalised COMMIT_EDITMSG, so reading it there would test
    # the PREVIOUS commit's message — worse than not checking. Closing that gap
    # needs a `commit-msg` hook; until then this coverage is honestly partial,
    # not silently assumed.
    if command:
        message = extract_commit_message(command)
        if message is not None and not is_valid_commit_message(message):
            log_error("on_commit", "COMMIT_MSG_VIOLATION", f"Non-conforming message: {message[:80]}")
            block("Commit message must follow Conventional Commits and end with the "
                  "#[Sprint_ID] suffix, e.g. \"feat(auth): add login flow #078\" (agents.md §5).")

        if message is not None:
            staged = get_staged_files()
            # Guard 3 (rules/code_craft.md §6): a bug fix ships its test.
            if reason := audit_regression_test(message, staged):
                log_error("on_commit", "REGRESSION_TEST_MISSING", message[:80])
                block(reason)
            # Guard 4 (rules/code_craft.md §7): a new dependency says why.
            if reason := audit_dependency_justification(message, staged):
                log_error("on_commit", "DEPENDENCY_UNJUSTIFIED", message[:80])
                block(reason)

    print("🛡️ [DEVOPS AGENT] Pre-Commit Integrity Handshake...")

    three_file_ok = audit_three_file_standard()
    if not three_file_ok:
        log_error("on_commit", "STRUCTURE_VIOLATION", "three_file_standard compliance check failed")

    secrets_ok = audit_secret_shielding()
    if not secrets_ok:
        log_error("on_commit", "SECRET_VIOLATION", "secret_sovereignty scrutiny detected vulnerabilities")

    if three_file_ok and secrets_ok:
        try:
            from hooks.state_mirror import mirror_active_state
            mirror_active_state()
        except ImportError:
            pass
        print("✅ [DEVOPS AGENT] PR_COMMIT_UNLOCKED: PASSED.")
        sys.exit(0)
    else:
        block("CRITICAL VIOLATION DETECTED. Commit blocked.")

if __name__ == "__main__":
    main()
