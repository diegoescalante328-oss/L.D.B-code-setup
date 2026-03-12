from __future__ import annotations

import pytest

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


load_settings = _load_attr("001_app/002_app_entrypoint.py", "load_settings")


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
    data = load_settings("002_config/002.002_runtime_settings.yaml")
    assert data["capture"]["interval_seconds"] == 3
