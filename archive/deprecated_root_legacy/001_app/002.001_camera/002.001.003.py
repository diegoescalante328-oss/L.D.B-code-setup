from __future__ import annotations


def parse_camera_source(raw: str | int) -> int | str:
    if isinstance(raw, int):
        return raw

    value = str(raw).strip()
    if value.isdigit():
        return int(value)
    return value
