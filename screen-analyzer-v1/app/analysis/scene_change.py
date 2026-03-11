from __future__ import annotations

import cv2
import numpy as np


def frame_difference_score(frame_a: np.ndarray, frame_b: np.ndarray) -> float:
    """
    Returns a normalized difference score between 0.0 and 1.0.
    Higher = more different.
    """
    if frame_a.shape != frame_b.shape:
        frame_b = cv2.resize(frame_b, (frame_a.shape[1], frame_a.shape[0]))

    gray_a = cv2.cvtColor(frame_a, cv2.COLOR_BGR2GRAY)
    gray_b = cv2.cvtColor(frame_b, cv2.COLOR_BGR2GRAY)

    diff = cv2.absdiff(gray_a, gray_b)
    score = float(np.mean(diff) / 255.0)
    return score


def is_meaningfully_different(
    frame_a: np.ndarray,
    frame_b: np.ndarray,
    threshold: float = 0.03,
) -> bool:
    return frame_difference_score(frame_a, frame_b) >= threshold