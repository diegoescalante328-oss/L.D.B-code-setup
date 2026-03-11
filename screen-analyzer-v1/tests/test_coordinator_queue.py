from __future__ import annotations

from app.queue_policy import LatestFrameBuffer


def test_latest_frame_wins() -> None:
    buffer = LatestFrameBuffer()

    should_start_1, frame_1 = buffer.enqueue("f1.jpg")
    should_start_2, _ = buffer.enqueue("f2.jpg")
    should_start_3, _ = buffer.enqueue("f3.jpg")

    assert should_start_1 is True
    assert frame_1 == "f1.jpg"
    assert should_start_2 is False
    assert should_start_3 is False

    next_frame = buffer.complete_and_pop_next()
    assert next_frame == "f3.jpg"

    final = buffer.complete_and_pop_next()
    assert final is None
    assert buffer.analysis_in_flight is False
