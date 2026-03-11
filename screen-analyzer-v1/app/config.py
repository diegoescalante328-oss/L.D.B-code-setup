from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass
class AppConfig:
    settings: dict[str, Any]

    @property
    def camera_source(self) -> str | int:
        return self.settings["camera"]["source"]


def load_settings(path: str | Path = "config/settings.yaml") -> dict[str, Any]:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    capture = data["capture"]
    interval = capture["interval_seconds"]
    min_interval = capture["min_interval_seconds"]
    max_interval = capture["max_interval_seconds"]
    if interval < min_interval or interval > max_interval:
        raise ValueError("capture.interval_seconds must be within [min_interval_seconds, max_interval_seconds]")
    if min_interval < 2 or max_interval > 10:
        raise ValueError("V1 interval range must stay within 2..10 seconds")
    if capture["max_in_flight_requests"] != 1:
        raise ValueError("V1 requires max_in_flight_requests == 1")
    return data
