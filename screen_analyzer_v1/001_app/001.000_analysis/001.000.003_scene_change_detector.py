from __future__ import annotations

import numpy as np


def _to_gray(frame: np.ndarray) -> np.ndarray:
    if frame.ndim == 2:
        return frame
    # assume BGR/RGB 3-channel image
    return frame.mean(axis=2).astype(np.uint8)


def _match_shape(frame: np.ndarray, shape: tuple[int, int]) -> np.ndarray:
    h, w = shape
    return frame[:h, :w]


def frame_difference_score(frame_a: np.ndarray, frame_b: np.ndarray) -> float:
    """Returns normalized difference score in [0, 1]."""
    gray_a = _to_gray(frame_a)
    gray_b = _to_gray(frame_b)

    h = min(gray_a.shape[0], gray_b.shape[0])
    w = min(gray_a.shape[1], gray_b.shape[1])
    if h == 0 or w == 0:
        return 1.0

    gray_a = _match_shape(gray_a, (h, w)).astype(np.int16)
    gray_b = _match_shape(gray_b, (h, w)).astype(np.int16)
    diff = np.abs(gray_a - gray_b)
    return float(np.mean(diff) / 255.0)


def is_meaningfully_different(frame_a: np.ndarray, frame_b: np.ndarray, threshold: float = 0.03) -> bool:
    return frame_difference_score(frame_a, frame_b) >= threshold
