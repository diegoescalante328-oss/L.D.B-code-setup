from __future__ import annotations

from pathlib import Path

import yaml


def load_system_prompt(prompt_config_path: str | Path = "config/prompts.yaml") -> str:
    data = yaml.safe_load(Path(prompt_config_path).read_text(encoding="utf-8"))
    prompt = data.get("analysis_system_prompt", "").strip()
    if not prompt:
        raise ValueError("analysis_system_prompt is missing or empty")
    return prompt
