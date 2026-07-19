# 🏭 Mass Standardizer

Automated engine for the batch normalization of the Universal-Agents technical arsenal.

## About The Project

The **Mass Standardizer** is the enforcement arm of technical sovereignty hardening. Its goal is to eliminate architectural debt through automated injection of the documentation and structure standards defined by `skill-creator`.

**Key Features:**
- **Audit & Detect**: Identifies skill folders that lack the official structure (dual Trinity Standard, agents.md §3).
- **Template Synthesis**: Injects standardized `README.md` and `SKILL.md` files.
- **Topological Enforcement**: For executable skills, guarantees the presence of the `/scripts/` directory and `__init__.py`.

## Getting Started

### Prerequisites
- Access to `manifest_skills.json`.
- Write permission on the flat `skills/` directory.

## Usage

Invoked during refactor sprints or full Matrix unification passes:

```bash
python skills/mass-standardizer/scripts/mass_standardizer.py --all
```

## License
Distributed under the MIT License.
