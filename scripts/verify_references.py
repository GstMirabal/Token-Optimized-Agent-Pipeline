"""Reference-integrity linter — immunizes the framework against the
"Master Ledger class" of inconsistency: normative references whose target
no longer exists or can never be reached.

Checks (run from the .agents root; CI fails the PR on any violation):
  (a) Every rules/*.md is reachable — referenced by name from agents.md,
      a workflow, or a command (lazy-loading requires a pointer somewhere).
  (b) Every *_TEMPLATE.md cited in agents.md/workflows/ exists in
      docs/standards/templates/.
  (c) Every numbered "Rule NN" citation resolves to an entry in
      rules/LEGACY_RULE_CONCORDANCE.md (the numbering system was abolished
      by the tabular refactor; unmapped numbers are phantom references).
  (d) Every workflow, script and executable skill has a declared invoker, or a
      declared exception (RA-16 INVOCATION_COVERAGE, agents.md §7).

invoked_by: Makefile `verify` target (and therefore .github/workflows/ci.yml).
"""
import ast
import json
import re
import sys
from pathlib import Path

CONCORDANCE = Path("rules/LEGACY_RULE_CONCORDANCE.md")
TEMPLATES_DIR = Path("docs/standards/templates")
EXCEPTIONS_FILE = Path("config/invocation_exceptions.json")

# Reasons an artifact may legitimately have no invoker inside the framework.
# A free-text reason is rejected: an exception nobody can categorise is an
# exception nobody will ever revisit.
VALID_EXCEPTION_REASONS = frozenset({
    "model-invoked",       # Claude invokes it by name from a conversation.
    "vendored-reference",  # Third-party material kept as reference, not wired.
    "human-entry-point",   # A person runs it directly; no framework caller.
    "one-time",            # A migration already consumed; kept for the record.
})

# History is never rewritten — legacy logs keep their citations un-audited.
# Generated/vendored runtime dirs are not normative material (absent in CI
# checkouts, but present locally: venvs, graph output, linked .claude trees).
SCAN_EXCLUDE = ("docs/roadmaps/", "docs/sprints/", "node_modules/", ".git/",
                "venv_skillopt/", "venv/", "graphify-out/", ".claude/",
                "CHANGELOG.md", str(CONCORDANCE))

LOADABLE = [Path("agents.md"), *Path("workflows").glob("*.md"), *Path("commands").glob("*.md")]


def loadable_text() -> str:
    return "\n".join(p.read_text(encoding="utf-8") for p in LOADABLE)


def scan_files():
    for pattern in ("**/*.md", "**/*.py"):
        for p in Path(".").glob(pattern):
            sp = str(p)
            if any(x in sp for x in SCAN_EXCLUDE):
                continue
            yield p


def check_rules_reachable(corpus: str) -> list[str]:
    errors = []
    for rule in sorted(Path("rules").glob("*.md")):
        if rule.name not in corpus:
            errors.append(f"(a) rules/{rule.name} is unreachable — nothing loadable references it.")
    return errors


# Filenames GitHub defines, which this framework does not own and never ships
# in docs/standards/templates/. Any workflow describing repository setup has to
# name them, and doing so is not a dangling reference.
PLATFORM_TEMPLATES = frozenset({
    "PULL_REQUEST_TEMPLATE.md",
    "ISSUE_TEMPLATE.md",
})


def check_templates_exist(corpus: str) -> list[str]:
    """Every framework template cited in a loadable document must exist.

    Args:
        corpus: Concatenated text of agents.md and every workflow.

    Returns:
        list[str]: One error per template cited without a file behind it.
    """
    errors = []
    for name in set(re.findall(r"([A-Z][A-Z_]*_TEMPLATE\.md)", corpus)):
        if name in PLATFORM_TEMPLATES:
            continue
        if not (TEMPLATES_DIR / name).exists():
            errors.append(f"(b) {name} is cited but missing from {TEMPLATES_DIR}/.")
    return errors


def check_rule_citations() -> list[str]:
    if not CONCORDANCE.exists():
        return [f"(c) {CONCORDANCE} missing — numbered citations cannot be resolved."]
    mapped = set(re.findall(r"\*\*Rule (\d+)", CONCORDANCE.read_text(encoding="utf-8")))
    # 41 covers 041/41.x style; normalize citations to their integer part.
    errors = []
    for p in scan_files():
        text = p.read_text(encoding="utf-8", errors="ignore")
        for num in re.findall(r"Rule[s]? 0*(\d+)(?:\.\d+)?", text):
            if num not in mapped:
                errors.append(f"(c) {p}: cites Rule {num}, not mapped in the concordance.")
    return sorted(set(errors))


def load_exceptions() -> tuple[dict[str, str], list[str]]:
    """Read the declared-exception registry and validate it against the tree.

    Exceptions live in a data file rather than in each artifact's frontmatter
    because vendored skills cannot be edited at all (Skill Documentation Veto,
    rules/skills_and_integrations.md §3).

    Returns:
        tuple[dict[str, str], list[str]]: path -> reason, plus registry errors.
    """
    if not EXCEPTIONS_FILE.exists():
        return {}, [f"(d) {EXCEPTIONS_FILE} missing — RA-16 cannot be evaluated."]

    errors: list[str] = []
    exceptions: dict[str, str] = {}
    for entry in json.loads(EXCEPTIONS_FILE.read_text(encoding="utf-8"))["exceptions"]:
        path, reason = entry["path"], entry["reason"]
        exceptions[path] = reason
        if reason not in VALID_EXCEPTION_REASONS:
            errors.append(
                f"(d) {EXCEPTIONS_FILE}: '{path}' has reason '{reason}', "
                f"not one of {sorted(VALID_EXCEPTION_REASONS)}."
            )
        # A stale exemption is worse than no exemption: it silently excuses an
        # artifact that no longer exists, and hides the next one to take its name.
        if not Path(path).exists():
            errors.append(f"(d) {EXCEPTIONS_FILE}: '{path}' does not exist — stale exemption.")
    return exceptions, errors


def imported_modules() -> set[str]:
    """Module names imported by any tracked Python file.

    A script imported as a module has an invoker even though its filename is
    never written anywhere. Missing this is not theoretical: `merge_json.py`
    looked orphaned to a filename-only scan while `scripts/install_claude.py`
    depends on it, and deleting it would have broken the bridge installer.
    """
    modules: set[str] = set()
    for path in [*Path("scripts").glob("*.py"), *Path("hooks").glob("*.py")]:
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules.add(node.module.split(".")[-1])
    return modules


def check_invocation_coverage(corpus: str) -> list[str]:
    """(d) Every mechanism declares an invoker, or a typed exception (RA-16).

    Args:
        corpus: Concatenated text of agents.md, workflows and commands.

    Returns:
        list[str]: One error per mechanism nothing invokes and nothing excuses.
    """
    exceptions, errors = load_exceptions()
    governance = corpus + "\n".join(
        p.read_text(encoding="utf-8")
        for p in [*Path("rules").glob("*.md"), *Path("agents").glob("*.md")]
    )
    modules = imported_modules()

    # Workflows and scripts are framework-owned: they declare their own invoker.
    for path in [*sorted(Path("workflows").glob("*.md")), *sorted(Path("scripts").glob("*.py"))]:
        key = str(path)
        if key in exceptions:
            continue
        if path.suffix == ".py" and path.stem in modules:
            continue
        if "invoked_by:" not in path.read_text(encoding="utf-8"):
            errors.append(
                f"(d) {key} declares no `invoked_by:` and has no exception — "
                f"a mechanism nothing calls is a regression, not a pending feature."
            )

    # Skills are not edited here: vendored SKILL.md files are under the
    # Documentation Veto, so a skill counts as invoked when governance names it.
    for skill in sorted(p for p in Path("skills").iterdir() if (p / "scripts").is_dir()):
        key = str(skill)
        if key in exceptions or skill.name in governance:
            continue
        errors.append(f"(d) {key} is an executable skill nothing invokes and nothing excuses.")

    return errors


def main() -> int:
    corpus = loadable_text()
    errors = (check_rules_reachable(corpus) + check_templates_exist(corpus)
              + check_rule_citations() + check_invocation_coverage(corpus))
    if errors:
        for e in errors:
            print(f"❌ {e}", file=sys.stderr)
        return 1
    print("✅ Reference integrity OK — rules reachable, templates exist, "
          "citations resolve, every mechanism has an invoker.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
