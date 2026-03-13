from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

from app.camera.stream_sources import parse_camera_source
from app.coordinator import Coordinator
from app.ui.dashboard import Dashboard


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _load_settings(repo_root: Path) -> dict[str, Any]:
    settings_path = repo_root / "config" / "settings.yaml"
    if not settings_path.exists():
        return {}

    data = yaml.safe_load(settings_path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def main() -> None:
    repo_root = _repo_root()
    load_dotenv(repo_root / ".env")
    settings = _load_settings(repo_root)

    camera_config = settings.get("camera", {})
    capture_config = settings.get("capture", {})
    analysis_config = settings.get("analysis", {})
    ui_config = settings.get("ui", {})

    raw_camera_source = os.getenv("CAMERA_SOURCE", str(camera_config.get("source", "0")))
    camera_source = parse_camera_source(raw_camera_source)
    capture_interval = float(os.getenv("CAPTURE_INTERVAL", capture_config.get("interval_seconds", 3)))
    schema_path = analysis_config.get("schema_path", "schemas/screen_analysis.schema.json")
    window_title = ui_config.get("window_title", "Screen Analyzer V1")
    skip_similar_frames = bool(capture_config.get("skip_similar_frames", True))

    dashboard = Dashboard(title=window_title)
    coordinator = Coordinator(
        dashboard=dashboard,
        camera_source=camera_source,
        capture_interval=capture_interval,
        schema_path=repo_root / schema_path,
        snapshot_dir=repo_root / "outputs" / "snapshots",
        log_file=repo_root / "logs" / "runtime.jsonl",
        skip_similar_frames=skip_similar_frames,
    )

    dashboard.set_on_close(coordinator.stop)

    try:
        coordinator.start()
    except Exception as exc:
        dashboard.set_status("Startup failed")
        dashboard.set_result("startup", f"Startup error:\n{exc}")

    try:
        dashboard.run()
    finally:
        coordinator.stop()


if __name__ == "__main__":
    main()
