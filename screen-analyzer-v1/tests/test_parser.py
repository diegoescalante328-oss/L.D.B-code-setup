from __future__ import annotations

import pytest

from app.analysis.parser import validate_analysis_payload


def test_validate_analysis_payload(schema_tmp_path) -> None:
    payload = {
        "screen_content": "A coding problem is visible.",
        "question_present": True,
        "main_answer": "The likely answer is 42.",
        "summary": "The screen contains a short coding prompt.",
        "readability": "clear",
        "needs_web_search": False,
        "notes": ["Image is readable."],
        "citations": [],
    }

    parsed = validate_analysis_payload(payload, schema_tmp_path)
    assert parsed["readability"] == "clear"


def test_validate_analysis_payload_raises_on_invalid(schema_tmp_path) -> None:
    bad = {
        "screen_content": "x",
        "question_present": True,
    }
    with pytest.raises(ValueError):
        validate_analysis_payload(bad, schema_tmp_path)
