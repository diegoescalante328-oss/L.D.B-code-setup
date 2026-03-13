from __future__ import annotations

from typing import Optional

import cv2
import numpy as np


class CameraStream:
    def __init__(self, source: int | str) -> None:
        self.source = source
        self.cap: Optional[cv2.VideoCapture] = None

    def open(self) -> None:
        self.cap = cv2.VideoCapture(self.source)
        if not self.cap.isOpened():
            self.release()
            raise RuntimeError(f"Camera could not be opened: {self.source}")

    def read(self) -> tuple[bool, np.ndarray | None]:
        if self.cap is None:
            return False, None
        ok, frame = self.cap.read()
        if not ok:
            return False, None
        return True, frame

    def release(self) -> None:
        if self.cap is not None:
            self.cap.release()
            self.cap = None
