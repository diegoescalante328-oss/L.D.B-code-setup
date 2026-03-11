from __future__ import annotations

import argparse
import json

from dotenv import load_dotenv

from app.analysis.openai_client import OpenAIAnalysisClient
from app.analysis.parser import validate_analysis_payload
from app.analysis.prompt_builder import load_system_prompt


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Analyze a single image frame.")
    parser.add_argument("--image", required=True, help="Path to image file")
    parser.add_argument("--schema", default="schemas/screen_analysis.schema.json")
    parser.add_argument("--prompt-config", default="config/prompts.yaml")
    parser.add_argument("--model", default="gpt-5.4")
    args = parser.parse_args()

    client = OpenAIAnalysisClient(model=args.model, schema_path=args.schema, image_detail="original")
    system_prompt = load_system_prompt(args.prompt_config)

    result = client.analyze_image_with_optional_web_search(args.image, system_prompt)
    parsed = validate_analysis_payload(result, args.schema)
    print(json.dumps(parsed, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
