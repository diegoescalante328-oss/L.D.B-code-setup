from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

import cv2
import numpy as np


@dataclass
class CameraStatus:
    connected: bool
    message: str


class CameraCapture:
    def __init__(self, source: int | str, startup_timeout_seconds: int = 30, reconnect_delay_seconds: int = 3) -> None:
        self.source = source
        self.startup_timeout_seconds = startup_timeout_seconds
        self.reconnect_delay_seconds = reconnect_delay_seconds
        self.cap: cv2.VideoCapture | None = None

    def connect(self) -> CameraStatus:
        deadline = time.time() + self.startup_timeout_seconds
        last_error = "unknown camera error"

        while time.time() < deadline:
            self.cap = cv2.VideoCapture(self.source)
            if self.cap.isOpened():
                ok, _ = self.cap.read()
                if ok:
                    return CameraStatus(True, "camera connected")
                last_error = "opened source but failed to read frame"
            else:
                last_error = "unable to open source"

            self.release()
            time.sleep(self.reconnect_delay_seconds)

        return CameraStatus(False, f"camera connection timeout: {last_error}")

    def read(self) -> tuple[bool, np.ndarray | None]:
        if self.cap is None:
            return False, None
        ok, frame = self.cap.read()
        if not ok:
            return False, None
        return True, frame

    def reconnect(self) -> CameraStatus:
        self.release()
        time.sleep(self.reconnect_delay_seconds)
        return self.connect()

    def release(self) -> None:
        if self.cap is not None:
            self.cap.release()
            self.cap = None
