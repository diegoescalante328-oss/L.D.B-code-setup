from __future__ import annotations

import cv2
import numpy as np


def _validate_frame(frame: np.ndarray, name: str) -> None:
    if not isinstance(frame, np.ndarray):
        raise TypeError(f"{name} must be a numpy array")
    if frame.size == 0:
        raise ValueError(f"{name} must not be empty")


def _prepare_frame(frame: np.ndarray, size: tuple[int, int] = (320, 180)) -> np.ndarray:
    _validate_frame(frame, "frame")

    if frame.ndim == 3:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    elif frame.ndim == 2:
        gray = frame
    else:
        raise ValueError("frame must have 2 or 3 dimensions")

    resized = cv2.resize(gray, size, interpolation=cv2.INTER_AREA)
    blurred = cv2.GaussianBlur(resized, (5, 5), 0)
    return blurred


def frame_difference_score(frame_a: np.ndarray, frame_b: np.ndarray) -> float:
    prepared_a = _prepare_frame(frame_a)
    prepared_b = _prepare_frame(frame_b)
    diff = cv2.absdiff(prepared_a, prepared_b)
    return float(np.mean(diff) / 255.0)


def changed_pixel_ratio(frame_a: np.ndarray, frame_b: np.ndarray, pixel_threshold: int = 20) -> float:
    prepared_a = _prepare_frame(frame_a)
    prepared_b = _prepare_frame(frame_b)
    diff = cv2.absdiff(prepared_a, prepared_b)
    changed = diff >= pixel_threshold
    return float(np.mean(changed))


def is_meaningfully_different(
    frame_a: np.ndarray,
    frame_b: np.ndarray,
    threshold: float = 0.02,
    pixel_ratio_threshold: float = 0.01,
) -> bool:
    mean_score = frame_difference_score(frame_a, frame_b)
    pixel_ratio = changed_pixel_ratio(frame_a, frame_b)
    return mean_score >= threshold or pixel_ratio >= pixel_ratio_threshold
