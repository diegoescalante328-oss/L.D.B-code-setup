from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv


def _load_attr(relative_path: str, attr: str):
    module_path = Path(__file__).resolve().parent / relative_path
    spec = importlib.util.spec_from_file_location(f"dynamic_{module_path.stem}", module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load module at {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, attr)


Coordinator = _load_attr("001_screen_analysis_coordinator.py", "Coordinator")
Dashboard = _load_attr("004.003_ui/004.003.001_dashboard.py", "Dashboard")


def load_settings(path: str | Path = "002_config/002.002_runtime_settings.yaml") -> dict[str, Any]:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    capture = data["capture"]
    interval = capture["interval_seconds"]
    min_interval = capture["min_interval_seconds"]
    max_interval = capture["max_interval_seconds"]
    if interval < min_interval or interval > max_interval:
        raise ValueError("capture.interval_seconds must be within [min_interval_seconds, max_interval_seconds]")
    if min_interval < 2 or max_interval > 10:
        raise ValueError("V1 interval range must stay within 2..10 seconds")
    if capture["max_in_flight_requests"] != 1:
        raise ValueError("V1 requires max_in_flight_requests == 1")
    return data


def main() -> None:
    load_dotenv()
    settings = load_settings("002_config/002.002_runtime_settings.yaml")

    dashboard = Dashboard()
    coordinator = Coordinator(dashboard=dashboard, settings=settings)
    coordinator.start()

    try:
        dashboard.run()
    finally:
        coordinator.stop()


if __name__ == "__main__":
    main()
