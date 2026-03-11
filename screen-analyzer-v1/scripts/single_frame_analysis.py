from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

from app.analysis.openai_client import OpenAIAnalysisClient
from app.analysis.parser import validate_analysis_payload


def load_prompt(prompt_path: str | Path) -> str:
    data = yaml.safe_load(Path(prompt_path).read_text(encoding="utf-8"))
    return data["analysis_system_prompt"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze a single image frame.")
    parser.add_argument("--image", required=True, help="Path to image file")
    parser.add_argument("--schema", default="schemas/screen_analysis.schema.json")
    parser.add_argument("--prompt-config", default="config/prompts.yaml")
    parser.add_argument("--model", default="gpt-5.4")
    args = parser.parse_args()

    system_prompt = load_prompt(args.prompt_config)

    client = OpenAIAnalysisClient(
        model=args.model,
        schema_path=args.schema,
        image_detail="original",
    )

    result = client.analyze_image_with_optional_web_search(
        image_path=args.image,
        system_prompt=system_prompt,
    )

    validate_analysis_payload(result, args.schema)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()