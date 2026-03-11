from __future__ import annotations


def parse_camera_source(raw: str) -> int | str:
    """
    Turns '0' into integer device index 0.
    Leaves URLs or other strings unchanged.
    """
    raw = raw.strip()
    if raw.isdigit():
        return int(raw)
    return raw