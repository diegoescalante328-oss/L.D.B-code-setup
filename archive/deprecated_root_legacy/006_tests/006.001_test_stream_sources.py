from app.camera.stream_sources import parse_camera_source


def test_parse_camera_source_numeric() -> None:
    assert parse_camera_source("0") == 0


def test_parse_camera_source_url() -> None:
    assert parse_camera_source("rtsp://example") == "rtsp://example"
