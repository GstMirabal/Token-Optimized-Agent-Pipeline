"""Data loader for the Agents rule optimization benchmark.

Loads the evaluation scenarios from the local JSON file and structures
them for the SkillOpt training loop.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from skillopt.datasets.base import SplitDataLoader


def _normalize_item(raw: dict[str, Any]) -> dict[str, Any]:
    """Normalizes a raw data item into the expected format for SkillOpt."""
    return {
        "id": str(raw.get("id") or ""),
        "question": str(raw.get("question") or ""),
        "ground_truth": str(raw.get("ground_truth") or ""),
        "task_type": str(raw.get("task_type") or "general_rule"),
    }


class AgentsOptDataLoader(SplitDataLoader):
    """Loads and splits the rule validation dataset for optimization."""

    def load_raw_items(self, data_path: str) -> list[dict[str, Any]]:
        """Loads items from the single JSON dataset path for ratio-based splitting."""
        path = Path(data_path)
        if not path.is_file():
            # If the path does not exist, return an empty list or try to locate it relative
            raise FileNotFoundError(f"Scenarios file not found at: {data_path}")

        with path.open(encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            raise ValueError(f"Expected a JSON list of items, got {type(data)}")

        return [_normalize_item(item) for item in data]

    def load_split_items(self, split_path: str) -> list[dict[str, Any]]:
        """Fallback split loader if pre-split directories are used."""
        path = Path(split_path)
        json_files = sorted(path.glob("*.json"))
        if json_files:
            with json_files[0].open(encoding="utf-8") as f:
                payload = json.load(f)
            if not isinstance(payload, list):
                raise ValueError(
                    f"Expected JSON array at top level of {json_files[0]}"
                )
            return [_normalize_item(row) for row in payload]

        raise FileNotFoundError(
            f"No .json file found in split path: {split_path}"
        )
