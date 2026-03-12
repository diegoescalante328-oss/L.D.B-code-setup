from __future__ import annotations

import numpy as np

import importlib.util
from pathlib import Path


def _load_attr(relative_path: str, attr: str):
    module_path = Path(__file__).resolve().parents[1] / relative_path
    spec = importlib.util.spec_from_file_location(f"dynamic_{module_path.stem}", module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load module at {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, attr)


frame_difference_score = _load_attr("001_app/001.000_analysis/001.000.003_scene_change_detector.py", "frame_difference_score")
is_meaningfully_different = _load_attr("001_app/001.000_analysis/001.000.003_scene_change_detector.py", "is_meaningfully_different")


def test_frame_difference_score_zero_for_identical_frames() -> None:
    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    assert frame_difference_score(frame, frame) == 0.0


def test_is_meaningfully_different_detects_change() -> None:
    frame_a = np.zeros((100, 100, 3), dtype=np.uint8)
    frame_b = np.ones((100, 100, 3), dtype=np.uint8) * 255
    assert is_meaningfully_different(frame_a, frame_b) is True