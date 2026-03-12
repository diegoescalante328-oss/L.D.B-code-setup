from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import cv2
import numpy as np


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dir(path: str | Path) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def save_frame(frame: np.ndarray, output_dir: str | Path, prefix: str = "frame") -> Path:
    output_dir = ensure_dir(output_dir)
    safe_ts = utc_timestamp().replace(":", "-")
    path = output_dir / f"{prefix}_{safe_ts}.jpg"
    ok = cv2.imwrite(str(path), frame)
    if not ok:
        raise IOError(f"Failed to save frame to {path}")
    return path


def crop_frame(frame: np.ndarray, x: int, y: int, w: int, h: int) -> np.ndarray:
    return frame[y : y + h, x : x + w]


def resize_for_preview(frame: np.ndarray, width: int = 640) -> np.ndarray:
    h, w = frame.shape[:2]
    if w <= width:
        return frame
    scale = width / float(w)
    return cv2.resize(frame, (int(w * scale), int(h * scale)))
