from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

from dotenv import load_dotenv


SCRIPT_DIR = Path(__file__).resolve().parent
APP_DIR = SCRIPT_DIR.parent / "001_app"


def _load_attr(relative_path: str, attr: str):
    module_path = APP_DIR / relative_path
    spec = importlib.util.spec_from_file_location(f"dynamic_{module_path.stem}", module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load module at {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, attr)


OpenAIAnalysisClient = _load_attr("001.000_analysis/001.000.000_openai_client.py", "OpenAIAnalysisClient")
validate_analysis_payload = _load_attr("001.000_analysis/001.000.001_response_parser.py", "validate_analysis_payload")
load_system_prompt = _load_attr("001.000_analysis/001.000.002_prompt_builder.py", "load_system_prompt")


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Analyze a single image frame.")
    parser.add_argument("--image", required=True, help="Path to image file")
    parser.add_argument("--schema", default="003_schemas/003.001_screen_analysis_schema.json")
    parser.add_argument("--prompt-config", default="002_config/002.001_prompt_settings.yaml")
    parser.add_argument("--model", default="gpt-5.4")
    args = parser.parse_args()

    client = OpenAIAnalysisClient(model=args.model, schema_path=args.schema, image_detail="original")
    system_prompt = load_system_prompt(args.prompt_config)

    result = client.analyze_image_with_optional_web_search(args.image, system_prompt)
    parsed = validate_analysis_payload(result, args.schema)
    print(json.dumps(parsed, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
