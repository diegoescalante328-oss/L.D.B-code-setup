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


parse_camera_source = _load_attr("001_app/002.001_camera/002.001.003_stream_sources.py", "parse_camera_source")


def test_parse_camera_source_device_index() -> None:
    assert parse_camera_source("0") == 0


def test_parse_camera_source_url() -> None:
    url = "rtsp://127.0.0.1:8554/live"
    assert parse_camera_source(url) == url
