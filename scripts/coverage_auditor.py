import os
import sys
import json
import subprocess

# 🧪 CryptoBot Coverage Auditor (Rule 76)
# Version: 1.1.0
# Logic: Block Sprint Closure if Unit Test Coverage is below 90% in targeted modules.

MIN_COVERAGE = 90.0

def audit_coverage():
    print("🧪 [COVERAGE AUDITOR] STARTING SECURITY CHECK...")
    
    # Run pytest with coverage for the targeted apps
    try:
        result = subprocess.run(
            ["pytest", "--cov=backend/apps", "--cov-report=json"],
            capture_output=True,
            text=True
        )
    except FileNotFoundError:
        print("🚨 Error: pytest not found. Execution blocked.")
        sys.exit(1)

    if not os.path.exists("coverage.json"):
        print("🚨 Error: coverage.json not generated. Verification failed.")
        sys.exit(1)

    with open("coverage.json") as f:
        data = json.load(f)

    total_pct = data.get("totals", {}).get("percent_covered", 0.0)

    print(f"📈 DETECTED COVERAGE: {total_pct}% (Target: {MIN_COVERAGE}%)")

    if total_pct < MIN_COVERAGE:
        print(f"🚨 [SECURITY BLOCK] COVERAGE REJECTED: {total_pct}% < {MIN_COVERAGE}%")
        print("❌ Sprint Closure is PROHIBITED until test requirements are liquidated.")
        sys.exit(1)
    
    print("✅ [SECURITY CLEAR] COVERAGE PASSED. READY FOR DEPLOYMENT.")
    sys.exit(0)

if __name__ == "__main__":
    audit_coverage()
