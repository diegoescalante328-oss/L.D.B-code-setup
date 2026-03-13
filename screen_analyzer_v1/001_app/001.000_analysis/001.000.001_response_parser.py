from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import ValidationError, validate


def load_schema(schema_path: str | Path) -> dict[str, Any]:
    path = Path(schema_path)
    if not path.exists():
        raise FileNotFoundError(f"Schema file not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def parse_structured_payload(payload: dict[str, Any] | str) -> dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, str):
        return json.loads(payload)
    raise TypeError(f"Unsupported payload type: {type(payload)!r}")


def validate_analysis_payload(payload: dict[str, Any] | str, schema_path: str | Path) -> dict[str, Any]:
    parsed = parse_structured_payload(payload)
    schema = load_schema(schema_path)
    try:
        validate(instance=parsed, schema=schema)
    except ValidationError as exc:
        raise ValueError(f"Structured output validation failed: {exc.message}") from exc
    return parsed
