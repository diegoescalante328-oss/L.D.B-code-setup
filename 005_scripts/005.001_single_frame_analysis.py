from __future__ import annotations

import argparse
import json
from pathlib import Path

from dotenv import load_dotenv

from app.analysis.openai_client import OpenAIAnalysisClient
from app.analysis.parser import validate_analysis_payload
from app.analysis.prompt_builder import build_system_prompt


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    load_dotenv(repo_root / ".env")

    parser = argparse.ArgumentParser(description="Analyze a single image frame.")
    parser.add_argument("--image", required=True, help="Path to a saved image")
    parser.add_argument("--schema", default=str(repo_root / "schemas" / "screen_analysis.schema.json"))
    args = parser.parse_args()

    client = OpenAIAnalysisClient(schema_path=args.schema)
    result = client.analyze_image_with_optional_web_search(
        image_path=args.image,
        system_prompt=build_system_prompt(repo_root / "config" / "prompts.yaml"),
    )
    validate_analysis_payload(result, args.schema)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
