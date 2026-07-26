#!/bin/zsh
# 🛡️ Kill Switch (Rule 67)
# Version: 1.0.0
# Logic: Restore the repository state upon critical failure or 3 consecutive errors.

echo "🚨 [KILL SWITCH] DEPLOYED. VERIFYING PIPELINE INTEGRITY..."

# Mandatory Safety Restoration
echo "🛠️ Restoring uncommitted changes in repository root..."
git restore .

# Clean untracked files in sensitive areas (optional, uncomment if safety level 3 needed)
# git clean -fd

echo "✅ [KILL SWITCH] RECOVERY COMPLETE. EXITING SESSION FOR SAFETY RE-ENTRY."
exit 1
