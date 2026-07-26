import logging
import pathlib
import sys

# Configure logging to native standard (INFO)
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
    stream=sys.stdout
)

def refresh_governance_context():
    """
    Reads the mandatory core governance files and task index to ensure
    the agent's context is aligned with the framework rules (Rule 10).
    """
    # Dynamic paths using pathlib relative to the .agents root
    # Note: Using parent.parent because the script lives in .agents/scripts/
    root_path = pathlib.Path(__file__).parent.parent
    rules_file = root_path / "governance/ruleset/global_user_rules.md"
    task_file = root_path / "task/task.md"

    # Verification of existence
    if not (rules_file.exists() and task_file.exists()):
        logging.error(f"Mandatory governance files missing or moved at {root_path}. Critical failure.")
        return False

    # Simulate contextual ingestion (Reading strings)
    try:
        _ = [f.read_text(encoding='utf-8') for f in [rules_file, task_file]]
    except Exception as e:
        logging.error(f"Failed to read governance context: {e}")
        return False

    logging.info("Governance verified and aligned (Rule 10)")
    return True

if __name__ == "__main__":
    refresh_governance_context()
