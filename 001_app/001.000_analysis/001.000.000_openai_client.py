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
        model: str | None = None,
        schema_path: str | Path = "schemas/screen_analysis.schema.json",
        image_detail: str | None = None,
    ) -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set.")

        self.model = model or os.getenv("OPENAI_MODEL", "gpt-5.4")
        self.image_detail = image_detail or os.getenv("IMAGE_DETAIL", "high")
        if self.image_detail not in {"auto", "low", "high"}:
            raise ValueError("IMAGE_DETAIL must be one of: auto, low, high")

        self.client = OpenAI(api_key=api_key)
        self.schema_path = Path(schema_path)
        if not self.schema_path.exists():
            raise FileNotFoundError(f"Schema file not found: {self.schema_path}")

        self.schema = json.loads(self.schema_path.read_text(encoding="utf-8"))

    @staticmethod
    def _image_to_data_url(image_path: str | Path) -> str:
        path = Path(image_path)
        if not path.exists():
            raise FileNotFoundError(f"Image file not found: {path}")

        mime_type, _ = mimetypes.guess_type(str(path))
        mime_type = mime_type or "image/jpeg"
        encoded = base64.b64encode(path.read_bytes()).decode("utf-8")
        return f"data:{mime_type};base64,{encoded}"

    def _build_input(self, image_path: str | Path, user_text: str) -> list[dict[str, Any]]:
        return [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": user_text},
                    {
                        "type": "input_image",
                        "image_url": self._image_to_data_url(image_path),
                        "detail": self.image_detail,
                    },
                ],
            }
        ]

    def _schema_format(self) -> dict[str, Any]:
        return {
            "format": {
                "type": "json_schema",
                "name": "screen_analysis",
                "schema": self.schema,
                "strict": True,
            }
        }

    @staticmethod
    def _parse_response_json(response: Any) -> dict[str, Any]:
        output_text = getattr(response, "output_text", None)
        if isinstance(output_text, str) and output_text.strip():
            return json.loads(output_text.strip())

        for item in getattr(response, "output", None) or []:
            if getattr(item, "type", None) != "message":
                continue
            for content in getattr(item, "content", None) or []:
                if getattr(content, "type", None) != "output_text":
                    continue
                text = getattr(content, "text", None)
                if isinstance(text, str) and text.strip():
                    return json.loads(text.strip())

        raise ValueError("Model returned no structured JSON text output.")

    def analyze_image(self, image_path: str | Path, system_prompt: str) -> dict[str, Any]:
        response = self.client.responses.create(
            model=self.model,
            instructions=system_prompt,
            input=self._build_input(
                image_path=image_path,
                user_text="Analyze this monitor image and return only structured JSON that matches the supplied schema.",
            ),
            text=self._schema_format(),
        )
        return self._parse_response_json(response)

    def analyze_image_with_optional_web_search(
        self,
        image_path: str | Path,
        system_prompt: str,
    ) -> dict[str, Any]:
        first_pass = self.analyze_image(image_path=image_path, system_prompt=system_prompt)
        if not first_pass.get("needs_web_search", False):
            return first_pass

        response = self.client.responses.create(
            model=self.model,
            instructions=system_prompt,
            tools=[{"type": "web_search"}],
            input=self._build_input(
                image_path=image_path,
                user_text=(
                    "Analyze this monitor image. Use web search only if current or external information is truly needed. "
                    "Return only structured JSON that matches the supplied schema."
                ),
            ),
            text=self._schema_format(),
            tool_choice="auto",
        )
        return self._parse_response_json(response)
