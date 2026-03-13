from __future__ import annotations

import pytest

import importlib.util
from pathlib import Path


def _load_attr(relative_path: str, attr: str):
    module_path = Path(__file__).resolve().parents[1] / relative_path
    spec = importlib.util.spec_from_file_location(f"dynamic_{module_path.stem}", module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load module at {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, attr)


validate_analysis_payload = _load_attr("001_app/001.000_analysis/001.000.001_response_parser.py", "validate_analysis_payload")


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
