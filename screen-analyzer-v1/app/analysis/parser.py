from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import validate


def load_schema(schema_path: str | Path) -> dict[str, Any]:
    path = Path(schema_path)
    if not path.exists():
        raise FileNotFoundError(f"Schema file not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def validate_analysis_payload(payload: dict[str, Any], schema_path: str | Path) -> dict[str, Any]:
    schema = load_schema(schema_path)
    validate(instance=payload, schema=schema)
    return payload