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
"""
import re
import sys
from pathlib import Path

CONCORDANCE = Path("rules/LEGACY_RULE_CONCORDANCE.md")
TEMPLATES_DIR = Path("docs/standards/templates")

# History is never rewritten — legacy logs keep their citations un-audited.
SCAN_EXCLUDE = ("docs/roadmaps/", "docs/sprints/", "node_modules/", ".git/",
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


def check_templates_exist(corpus: str) -> list[str]:
    errors = []
    for name in set(re.findall(r"([A-Z][A-Z_]*_TEMPLATE\.md)", corpus)):
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


def main() -> int:
    corpus = loadable_text()
    errors = check_rules_reachable(corpus) + check_templates_exist(corpus) + check_rule_citations()
    if errors:
        for e in errors:
            print(f"❌ {e}", file=sys.stderr)
        return 1
    print("✅ Reference integrity OK — rules reachable, templates exist, all numbered citations resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
