import os
import sys

# 🛡️ CryptoBot Legacy App Auditor (Rule 10/36/71)
# Version: 1.0.0
# Logic: Verify that backend/apps/ contains EXACTLY the 11 Constitutional Apps.

APPS_DIR = "backend/apps/"
# Master Architecture List (Approved by Agente Principal)
CONSTITUTIONAL_APPS = [
    "core", "datafeed", "live_trading", "notifications", 
    "portfolio_reporting", "risk_control", "strategies", 
    "technical_analysis", "trades", "users", "workbench"
]

def audit_legacy_apps():
    print("🔍 [LEGACY AUDITOR] ANALYZING BACKEND ARCHITECTURE...")
    
    if not os.path.exists(APPS_DIR):
        print(f"🚨 Error: Apps directory {APPS_DIR} not found.")
        sys.exit(1)

    existing_apps = [name for name in os.listdir(APPS_DIR) 
                    if os.path.isdir(os.path.join(APPS_DIR, name)) 
                    and name not in ["__pycache__", ".DS_Store"]]

    errors = 0
    # 1. Detection of unauthorized (Shadow) Apps
    for app in existing_apps:
        if app not in CONSTITUTIONAL_APPS:
            print(f"❌ [SHADOW APP DETECTED]: '{app}' is NOT in the Master Architectural Flow. Rule 10 Violation!")
            errors += 1
        else:
            print(f"✅ Verified Module: apps.{app}")

    # 2. Identification of missing core apps
    for app in CONSTITUTIONAL_APPS:
        if app not in existing_apps:
            print(f"⚠️ Warning: Constitutional App '{app}' is missing from backend/apps/.")
            errors += 1

    if errors > 0:
        print(f"🚨 [AUDIT FAILED]: {errors} Legacy/Architecture conflicts detected.")
        sys.exit(1)
    
    print("✨ [AUDIT PASSED]: Project Backend matches the 100% Constitutional Design.")
    sys.exit(0)

if __name__ == "__main__":
    audit_legacy_apps()
