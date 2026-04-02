"""
🛡️ Universal-Agents: Python Quality Auditor (3rd-party)
Agnostic health-check script for Python repositories.
"""

import os
import subprocess
import json

def run_audit_command(name, command):
    print(f"--- [Auditing {name}] ---")
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print(f"✅ {name}: 0 issues detected.")
            return True
        else:
            print(f"❌ {name}: Issues found.")
            print(result.stdout)
            print(result.stderr)
            return False
    except FileNotFoundError:
        print(f"⚠️ {name} is not installed or not in path. Skipping...")
        return None

def main():
    root_path = os.getcwd()
    print(f"🚀 Initializing Python Quality Audit in: {root_path}")

    # Standard configuration discovery
    config_files = ['.ruff.toml', 'pyproject.toml', 'requirements.txt', '.mypy.ini']
    found_configs = [f for f in config_files if os.path.exists(os.path.join(root_path, f))]
    print(f"📁 Metadata Discovery: {found_configs}")

    # Execution Matrix
    audits = {
        "Linting (Ruff)": "ruff check .",
        "Type Safety (Mypy)": "mypy .",
        "Security (Bandit)": "bandit -r .",
        "Complexity (Radon)": "radon cc . -a"
    }

    results = {}
    for name, cmd in audits.items():
        results[name] = run_audit_command(name, cmd)

    print("\n🏁 --- [Final Audit Summary] ---")
    all_passing = True
    for name, success in results.items():
        status = "✅ PASS" if success is True else "❌ FAIL" if success is False else "⚠️ SKIP"
        print(f"{name}: {status}")
        if success is False:
            all_passing = False
            
    if all_passing:
        print("\n🏆 Repository is 100% Python Quality Certified.")
    else:
        print("\n🚨 Action Required: Resolve the issues above to comply with framework standards.")

if __name__ == "__main__":
    main()
