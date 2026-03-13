from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np


def save_snapshot(frame: np.ndarray, path: str | Path) -> str:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    ok = cv2.imwrite(str(output_path), frame)
    if not ok:
        raise IOError(f"Failed to write snapshot to {output_path}")
    return str(output_path)
