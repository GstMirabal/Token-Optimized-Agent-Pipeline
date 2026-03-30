# Knowledge Item: Python 3.13 & Django-Stubs Stability vs. Mypy

## Context
During the **Global Certification Audit (Sprint 002)** for the CryptoBot project, we attempted to achieve 100% type safety using Mypy in a **Python 3.13** environment with `django-stubs`.

## The Blockage
Mypy triggered an **INTERNAL ERROR** (specifically in `django-stubs/http/request.pyi:63`) when attempting to audit the project. This is a known incompatibility between the current version of `django-stubs` and the latest Python 3.13 internals.

```text
/Users/gstmirabal/Developer/GitHub/Cryptobot/venv/lib/python3.13/site-packages/django-stubs/http/request.pyi:63: error: INTERNAL ERROR -- Please try using mypy master on GitHub
```

## The Solution
To maintain CI/CD stability and continue auditing the rest of the project without being blocked by external library failures, we implemented an exclusion rule in `pyproject.toml`.

```toml
[tool.mypy]
python_version = "3.13"
exclude = ["django-stubs"]  # Patch to bypass unstable stubs in Python 3.13
# ... rest of configuration
```

Additionally, it is established that for any terminal operation requiring `config.toml` resolution via `envtoml`, the environment variables MUST be exported first (using the integrated `Makefile` is the recommended path).

```bash
# Recommended command execution
make lint
make type-check
```

---
`Extracted by Antigravity AI - Amnesia Protocol 2026-03-30`
