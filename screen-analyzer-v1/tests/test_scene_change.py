from __future__ import annotations

import numpy as np

from app.analysis.scene_change import frame_difference_score, is_meaningfully_different


def test_frame_difference_score_zero_for_identical_frames() -> None:
    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    assert frame_difference_score(frame, frame) == 0.0


def test_is_meaningfully_different_detects_change() -> None:
    frame_a = np.zeros((100, 100, 3), dtype=np.uint8)
    frame_b = np.ones((100, 100, 3), dtype=np.uint8) * 255
    assert is_meaningfully_different(frame_a, frame_b) is True