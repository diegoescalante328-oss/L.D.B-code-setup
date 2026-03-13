from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def append_jsonl(log_path: str | Path, record: dict[str, Any]) -> None:
    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")
        file.flush()
