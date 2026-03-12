from __future__ import annotations

from urllib.parse import urlparse


def is_url_source(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https", "rtsp", "rtmp"} and bool(parsed.netloc)


def parse_camera_source(raw: str | int) -> int | str:
    """Accept either webcam index (int-like) or stream URL."""
    if isinstance(raw, int):
        return raw

    text = str(raw).strip()
    if text == "":
        raise ValueError("Camera source cannot be empty")

    if text.isdigit() or (text.startswith("-") and text[1:].isdigit()):
        return int(text)

    if is_url_source(text):
        return text

    # fall back to raw string for local paths/device aliases supported by OpenCV
    return text
