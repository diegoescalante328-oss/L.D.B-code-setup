from __future__ import annotations

import base64
import json
import mimetypes
import os
from pathlib import Path
from typing import Any

from openai import OpenAI


class OpenAIAnalysisClient:
    """
    Minimal OpenAI Responses API wrapper for screen analysis.

    Expected environment:
        OPENAI_API_KEY=...
    """

    def __init__(
        self,
        model: str = "gpt-5.4",
        schema_path: str | Path = "schemas/screen_analysis.schema.json",
        image_detail: str = "original",
    ) -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set.")

        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.image_detail = image_detail
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
        if mime_type is None:
            mime_type = "image/jpeg"

        raw = image_path.read_bytes()
        encoded = base64.b64encode(raw).decode("utf-8")
        return f"data:{mime_type};base64,{encoded}"

    def analyze_image(
        self,
        image_path: str | Path,
        system_prompt: str,
    ) -> dict[str, Any]:
        """
        Send one image for analysis and return parsed JSON.
        """
        data_url = self._image_to_data_url(image_path)

        response = self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": system_prompt,
                        }
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": (
                                "Analyze this monitor image and return only structured JSON "
                                "that matches the provided schema."
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
        )

        text_output = getattr(response, "output_text", None)
        if not text_output:
            raise ValueError("Model returned no structured text output.")

        return json.loads(text_output)

    def analyze_image_with_optional_web_search(
        self,
        image_path: str | Path,
        system_prompt: str,
    ) -> dict[str, Any]:
        """
        First pass: no web search.
        If model says needs_web_search = True, do a second pass with web_search enabled.
        """
        first_pass = self.analyze_image(image_path=image_path, system_prompt=system_prompt)

        if not first_pass.get("needs_web_search", False):
            return first_pass

        data_url = self._image_to_data_url(image_path)

        response = self.client.responses.create(
            model=self.model,
            tools=[{"type": "web_search"}],
            input=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": system_prompt,
                        }
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": (
                                "Analyze this monitor image. "
                                "Use web search only if needed for current information. "
                                "Return only structured JSON matching the provided schema."
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
        )

        text_output = getattr(response, "output_text", None)
        if not text_output:
            raise ValueError("Second-pass model returned no structured text output.")

        return json.loads(text_output)