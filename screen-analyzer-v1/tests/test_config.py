from __future__ import annotations

import pytest

from app.config import load_settings


def test_settings_interval_validation(tmp_path) -> None:
    cfg = tmp_path / "settings.yaml"
    cfg.write_text(
        """
app: {name: test, log_dir: logs, snapshot_dir: outputs}
camera: {source: 0, startup_timeout_seconds: 30}
capture: {interval_seconds: 11, min_interval_seconds: 2, max_interval_seconds: 10, max_in_flight_requests: 1}
analysis: {model: gpt-5.4}
ui: {stale_after_seconds: 15}
recovery: {reconnect_delay_seconds: 3}
""",
        encoding="utf-8",
    )
    with pytest.raises(ValueError):
        load_settings(cfg)


def test_settings_loads_defaults() -> None:
    data = load_settings("config/settings.yaml")
    assert data["capture"]["interval_seconds"] == 3


def test_settings_requires_latest_frame_wins(tmp_path) -> None:
    cfg = tmp_path / "settings.yaml"
    cfg.write_text(
        """
app: {name: test, log_dir: logs, snapshot_dir: outputs}
camera: {source: 0, startup_timeout_seconds: 30}
capture: {interval_seconds: 3, min_interval_seconds: 2, max_interval_seconds: 10, max_in_flight_requests: 1, latest_frame_wins: false}
analysis: {model: gpt-5.4}
ui: {stale_after_seconds: 15}
recovery: {reconnect_delay_seconds: 3}
""",
        encoding="utf-8",
    )
    with pytest.raises(ValueError):
        load_settings(cfg)
