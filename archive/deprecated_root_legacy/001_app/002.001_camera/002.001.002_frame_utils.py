from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import cv2
import numpy as np


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def ensure_dir(path: str | Path) -> Path:
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def safe_timestamp_for_filename() -> str:
    return utc_timestamp().replace(":", "-").replace("+00:00", "Z")


def save_frame(frame: np.ndarray, output_dir: str | Path, prefix: str = "frame") -> Path:
    if frame is None or not isinstance(frame, np.ndarray):
        raise ValueError("frame must be a valid numpy array")

    output_dir = ensure_dir(output_dir)
    filename = f"{prefix}_{safe_timestamp_for_filename()}.jpg"
    path = output_dir / filename
    ok = cv2.imwrite(str(path), frame)
    if not ok:
        raise IOError(f"Failed to save frame to {path}")
    return path


def crop_frame(frame: np.ndarray, x: int, y: int, w: int, h: int) -> np.ndarray:
    if frame is None or not isinstance(frame, np.ndarray):
        raise ValueError("frame must be a valid numpy array")
    if w <= 0 or h <= 0:
        raise ValueError("w and h must be positive")

    frame_height, frame_width = frame.shape[:2]
    x1 = max(0, x)
    y1 = max(0, y)
    x2 = min(frame_width, x + w)
    y2 = min(frame_height, y + h)
    if x1 >= x2 or y1 >= y2:
        raise ValueError("crop region is outside frame bounds")
    return frame[y1:y2, x1:x2]
