# Cursor-era execution audit (026–033)

Derived by `scripts/audit_cursor_era.py`. Do not edit by hand.

| Sprint | CE-1 | CE-2 | CE-3 | CE-4 |
| :--- | ---: | ---: | ---: | ---: |
| 026 | 52 | 0 | 2 | 0 |
| 027 | 25 | 0 | 2 | 0 |
| 028 | 3 | 0 | 2 | 0 |
| 029 | 8 | 0 | 2 | 0 |
| 030 | 13 | 0 | 0 | 0 |
| 031 | 5 | 0 | 0 | 0 |
| 032 | 3 | 0 | 0 | 0 |
| 033 | 0 | 0 | 0 | 0 |

## CE-5 — sandbox vs non-sandbox pytest protocol

Do not record live pass/fail counts here: sandbox denial of
`git init` produces false reds, and a live count needs a clean
environment that this census must not assume. Reproduce both
sides with the same invocation:

```bash
# Outside sandbox (git init allowed) — suite should pass:
./venv_skillopt/bin/python3 -m pytest tests/ -q; echo $?

# Inside Cursor sandbox (git init may be denied) — compare:
./venv_skillopt/bin/python3 -m pytest tests/ -q; echo $?
```

If the sandbox run fails with git-init permission errors while the
non-sandbox run passes, treat the red as CE-5 (measurement noise),
not a suite regression.
