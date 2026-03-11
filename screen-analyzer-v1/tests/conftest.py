from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture
def schema_tmp_path(tmp_path):
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "ScreenAnalysis",
        "type": "object",
        "properties": {
            "screen_content": {"type": "string"},
            "question_present": {"type": "boolean"},
            "main_answer": {"type": "string"},
            "summary": {"type": "string"},
            "readability": {
                "type": "string",
                "enum": ["clear", "partial", "unreadable"],
            },
            "needs_web_search": {"type": "boolean"},
            "notes": {"type": "array", "items": {"type": "string"}},
            "citations": {"type": "array", "items": {"type": "string"}},
        },
        "required": [
            "screen_content",
            "question_present",
            "main_answer",
            "summary",
            "readability",
            "needs_web_search",
            "notes",
            "citations",
        ],
        "additionalProperties": False,
    }

    path = tmp_path / "screen_analysis.schema.json"
    path.write_text(json.dumps(schema), encoding="utf-8")
    return path
