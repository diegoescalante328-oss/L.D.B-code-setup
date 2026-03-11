from __future__ import annotations

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

    validate_analysis_payload(payload, schema_tmp_path)