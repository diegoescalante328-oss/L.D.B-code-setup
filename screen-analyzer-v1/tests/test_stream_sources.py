from __future__ import annotations

from app.camera.stream_sources import parse_camera_source


def test_parse_camera_source_device_index() -> None:
    assert parse_camera_source("0") == 0


def test_parse_camera_source_url() -> None:
    url = "rtsp://127.0.0.1:8554/live"
    assert parse_camera_source(url) == url
