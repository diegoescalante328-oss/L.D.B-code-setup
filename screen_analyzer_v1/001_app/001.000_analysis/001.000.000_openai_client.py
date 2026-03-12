from __future__ import annotations

import base64
import json
import mimetypes
import os
from pathlib import Path
from typing import Any

from openai import OpenAI


class OpenAIAnalysisClient:
    def __init__(
        self,
        model: str = "gpt-5.4",
        schema_path: str | Path = "003_schemas/003.001_screen_analysis_schema.json",
        image_detail: str = "original",
        enable_web_search_second_pass: bool = True,
    ) -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set.")

        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.image_detail = image_detail
        self.enable_web_search_second_pass = enable_web_search_second_pass
        self.schema_path = Path(schema_path)

        if not self.schema_path.exists():
            raise FileNotFoundError(f"Schema file not found: {self.schema_path}")
        self.schema = json.loads(self.schema_path.read_text(encoding="utf-8"))

    @staticmethod
    def _image_to_data_url(image_path: str | Path) -> str:
        image_path = Path(image_path)
        if not image_path.exists():
            raise FileNotFoundError(f"Image file not found: {image_path}")

        mime_type, _ = mimetypes.guess_type(str(image_path))
        mime_type = mime_type or "image/jpeg"

        raw = image_path.read_bytes()
        encoded = base64.b64encode(raw).decode("utf-8")
        return f"data:{mime_type};base64,{encoded}"

    def _create_request(self, data_url: str, system_prompt: str, use_web_search: bool = False):
        kwargs: dict[str, Any] = {}
        if use_web_search:
            kwargs["tools"] = [{"type": "web_search"}]

        return self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "system",
                    "content": [{"type": "input_text", "text": system_prompt}],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": (
                                "Analyze this monitor image and return only structured JSON "
                                "matching the supplied schema."
                            ),
                        },
                        {
                            "type": "input_image",
                            "image_url": data_url,
                            "detail": self.image_detail,
                        },
                    ],
                },
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "screen_analysis",
                    "schema": self.schema,
                    "strict": True,
                }
            },
            **kwargs,
        )

    def _parse_text_output(self, response, error_prefix: str) -> dict[str, Any]:
        text_output = getattr(response, "output_text", None)
        if not text_output:
            raise ValueError(f"{error_prefix} returned no structured text output.")
        return json.loads(text_output)

    def analyze_image(self, image_path: str | Path, system_prompt: str) -> dict[str, Any]:
        data_url = self._image_to_data_url(image_path)
        response = self._create_request(data_url=data_url, system_prompt=system_prompt, use_web_search=False)
        return self._parse_text_output(response, "First pass")

    def analyze_image_with_optional_web_search(self, image_path: str | Path, system_prompt: str) -> dict[str, Any]:
        first_pass = self.analyze_image(image_path=image_path, system_prompt=system_prompt)
        if not self.enable_web_search_second_pass:
            return first_pass
        if not first_pass.get("needs_web_search", False):
            return first_pass

        data_url = self._image_to_data_url(image_path)
        response = self._create_request(data_url=data_url, system_prompt=system_prompt, use_web_search=True)
        return self._parse_text_output(response, "Second pass")
