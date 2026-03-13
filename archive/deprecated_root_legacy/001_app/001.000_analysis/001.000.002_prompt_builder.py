from __future__ import annotations

from pathlib import Path

import yaml


DEFAULT_SYSTEM_PROMPT = (
    "You are a careful screen analysis assistant. "
    "Analyze the provided monitor image and return only JSON that matches the supplied schema. "
    "Be concise, concrete, and grounded in what is visible. "
    "If the image is hard to read, reflect that in readability and notes. "
    "Only set needs_web_search to true when current or external information is genuinely needed."
)


def build_system_prompt(config_path: str | Path = "config/prompts.yaml") -> str:
    path = Path(config_path)
    if not path.exists():
        return DEFAULT_SYSTEM_PROMPT

    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception:
        return DEFAULT_SYSTEM_PROMPT

    value = data.get("screen_analysis_system_prompt")
    return value.strip() if isinstance(value, str) and value.strip() else DEFAULT_SYSTEM_PROMPT
