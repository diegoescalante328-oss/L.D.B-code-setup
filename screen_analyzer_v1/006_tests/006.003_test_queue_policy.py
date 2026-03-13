from __future__ import annotations

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


LatestFrameBuffer = _load_attr("001_app/001_screen_analysis_coordinator.py", "LatestFrameBuffer")


def test_latest_frame_wins() -> None:
    buffer = LatestFrameBuffer()

    should_start_1, frame_1 = buffer.enqueue("f1.jpg", "t1")
    should_start_2, _ = buffer.enqueue("f2.jpg", "t2")
    should_start_3, _ = buffer.enqueue("f3.jpg", "t3")

    assert should_start_1 is True
    assert frame_1 == {"frame_path": "f1.jpg", "capture_ts": "t1"}
    assert should_start_2 is False
    assert should_start_3 is False

    next_frame = buffer.complete_and_pop_next()
    assert next_frame == {"frame_path": "f3.jpg", "capture_ts": "t3"}

    final = buffer.complete_and_pop_next()
    assert final is None
    assert buffer.analysis_in_flight is False
