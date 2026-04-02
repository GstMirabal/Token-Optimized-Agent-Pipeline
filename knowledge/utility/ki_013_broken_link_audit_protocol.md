# KI-013: Post-Relocation Link Integrity Protocol

## Status
- **ID:** ki-013
- **Domain:** utility
- **Tactical Logic:** Navigation Protection post-structural mutation.
- **Rule Origin:** Rule 21, 78 (Institutional Identity & Persistent Metadata).

## The Problem
Hierarchical restructuring (moving rules to subdirectories like `/constitution/`) often causes "Silent Context Erosion" by breaking markdown links in root READMEs, workflows, and rule sets. Standard IDE refactoring tools often miss these relative or absolute paths inside a submodule.

## The Heuristic (Protocol)
Whenever a core directory within `.agents/` is moved or renamed, the Agent MUST execute a **Global Integrity Grep**:

```bash
# 1. Search for broken relative links
grep -rnEi "governance/|skills/|task/" .agents/

# 2. Repair strategically using Atomic Replace
# (Correcting to the new hierarchical path)
```

## Implementation History
- **Case #14b9868e:** Movement of Governance rules to `/constitution/` broke 4 critical links in the root README and two Skill files. Detection was only possible via manual grep.

## Verification
- Confirm that no internal document within the framework yields a 404-style error during AI or Human navigation.
