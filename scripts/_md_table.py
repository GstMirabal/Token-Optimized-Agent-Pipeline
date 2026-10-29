"""Split one Markdown table row into cells, honouring the ``\\|`` escape.

Three scripts split rows with a plain string split on the pipe character, so an escaped pipe inside
a cell cut that cell in two and shifted every column after it (`KI-057-3`).
`scripts/check_task_scope.py` already held the correct splitter as a private
``_cells``; this module is its single home so the callers share one definition
(`rules/code_craft.md §1`: extraction at the second call site).

The helper strips whitespace only. A caller that also wants backticks removed
applies ``.strip("`")`` to each returned cell, which keeps each caller's
pre-existing behaviour exactly.

invoked_by: scripts/check_task_scope.py, scripts/check_gate_log.py,
scripts/check_forge_ladder.py, scripts/detect_new_models.py.

Usage:
    from _md_table import split_cells
"""

from __future__ import annotations

import re

_UNESCAPED_PIPE = re.compile(r"(?<!\\)\|")


def split_cells(line: str) -> list[str]:
    """Split a Markdown table row into cells, honouring the ``\\|`` escape.

    Args:
        line: One raw table row.

    Returns:
        list[str]: Whitespace-stripped cells; an escaped pipe stays inside its
        cell as a plain ``|``.
    """
    body = line.strip().removeprefix("|").removesuffix("|")
    return [part.replace("\\|", "|").strip() for part in _UNESCAPED_PIPE.split(body)]
