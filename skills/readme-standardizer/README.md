# README Standardizer

Ensures all documentation files follow the official Technical English and Institutional Identity standards.

## About The Project

The **README Standardizer** is the Matrix's institutional-identity alignment tool. It ensures every documentation file (README.md, SKILL.md) keeps a professional, coherent appearance through master templates ("Gold Standard"), in compliance with **Rule 78**.

**Key Features:**
*   **Gold Standard Template:** Injects institutional templates with dynamic placeholders.
*   **Institutional Badges:** Centralized management of status, license, and professional-profile shields.
*   **Atomic Navigation:** Automates critical sections such as Table of Contents and Back to Top.

## Getting Started

### Prerequisites

*   **Universal-Agents Submodule**: Access to the assets folder is required to retrieve the master templates.

### Installation & Configuration

1. **Integrated in Core**
   Located at `.agents/skills/readme-standardizer/`.

2. **Template access**
   Master templates live in `./assets/template.md`.

## Usage

Invoked when the arsenal needs standardizing or a Rule 78 violation is detected in the documentation of the root project or its submodules:

```bash
# Example: applying the master template to a specific README
Principal Agent: "Standardize this repository based on Rule 78."
```
