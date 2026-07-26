# JS-Standardizer

Universal alignment for JS/TS projects (ESLint, Prettier, JSDoc) ensuring legal governance compliance.

## About The Project

The **JS-Standardizer** is the pipeline's universal alignment tool for JavaScript and TypeScript projects. It ensures code complies with the framework's quality standards (ESLint, Prettier) and that internal documentation stays legally coherent through mandatory JSDoc.

**Key Features:**
*   **Linter Automation:** Ready-to-use ESLint and Prettier configuration aligned with **Rule 35**.
*   **TS Support:** Native TypeScript integration for modern architectures.
*   **JSDoc Guard:** Validates the presence of documentation signatures on all core functions.

### Built With

![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![TypeScript](https://img.shields.io/badge/typescript-%23007ACC.svg?style=for-the-badge&logo=typescript&logoColor=white)
![ESLint](https://img.shields.io/badge/eslint-3A33D1?style=for-the-badge&logo=eslint&logoColor=white)

## Getting Started

### Prerequisites

*   **Node.js**: Required to run the linters and standardizers.

### Installation & Configuration

1. **Integrated in Core**
   Located at `.agents/skills/js-standardizer/`.

2. **Link local project**
   Make sure the host project root has a `package.json` so rule injection can take place.

## Usage

Invoked automatically during incremental audit phases (`/agents:audit`):

```bash
# Example: standardizing files under src/
pnpm run lint --fix
```
