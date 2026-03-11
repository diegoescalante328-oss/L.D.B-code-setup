from __future__ import annotations

import threading
import time
from pathlib import Path
from typing import Any

from app.analysis.openai_client import OpenAIAnalysisClient
from app.analysis.parser import validate_analysis_payload
from app.analysis.prompt_builder import load_system_prompt
from app.analysis.scene_change import is_meaningfully_different
from app.camera.capture import CameraCapture
from app.camera.frame_utils import crop_frame, save_frame, utc_timestamp
from app.camera.stream_sources import parse_camera_source
from app.storage.logs import append_jsonl
from app.queue_policy import LatestFrameBuffer


class Coordinator:
    def __init__(self, dashboard, settings: dict[str, Any], schema_path: str = "schemas/screen_analysis.schema.json") -> None:
        self.dashboard = dashboard
        self.settings = settings
        self.schema_path = schema_path

        camera_cfg = settings["camera"]
        capture_cfg = settings["capture"]
        app_cfg = settings["app"]
        recovery_cfg = settings["recovery"]

        self.capture_interval = float(capture_cfg["interval_seconds"])
        self.skip_similar = bool(capture_cfg.get("skip_similar_frames", True))

        self.snapshot_dir = Path(app_cfg["snapshot_dir"]) / "snapshots"
        self.log_file = Path(app_cfg["log_dir"]) / "runtime.jsonl"

        self.camera = CameraCapture(
            source=parse_camera_source(camera_cfg["source"]),
            startup_timeout_seconds=int(camera_cfg.get("startup_timeout_seconds", 30)),
            reconnect_delay_seconds=int(recovery_cfg.get("reconnect_delay_seconds", 3)),
        )

        self.analysis_client = OpenAIAnalysisClient(
            model=settings["analysis"].get("model", "gpt-5.4"),
            schema_path=schema_path,
            image_detail=settings["analysis"].get("image_detail", "original"),
        )
        self.system_prompt = load_system_prompt()

        self.running = False
        self.capture_thread: threading.Thread | None = None
        self.buffer = LatestFrameBuffer()
        self.last_frame = None
        self.last_result_at = 0.0
        self.state_lock = threading.Lock()

    def start(self) -> None:
        self.dashboard.set_status("connecting")
        status = self.camera.connect()
        if not status.connected:
            self.dashboard.set_error(status.message)
            raise RuntimeError(status.message)

        self.running = True
        self.dashboard.set_status("idle")
        self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.capture_thread.start()

    def stop(self) -> None:
        self.running = False
        self.camera.release()

    def _capture_loop(self) -> None:
        while self.running:
            cycle_start = time.time()
            capture_ts = utc_timestamp()
            ok, frame = self.camera.read()
            if not ok or frame is None:
                self.dashboard.set_error("camera read failure; reconnecting")
                reconnect_status = self.camera.reconnect()
                if reconnect_status.connected:
                    self.dashboard.set_status("idle")
                else:
                    self.dashboard.set_error(reconnect_status.message)
                continue

            crop_cfg = self.settings.get("crop")
            if crop_cfg and crop_cfg.get("enabled"):
                frame = crop_frame(frame, crop_cfg["x"], crop_cfg["y"], crop_cfg["w"], crop_cfg["h"])

            self.dashboard.update_feed(frame)

            stale_after = int(self.settings["ui"].get("stale_after_seconds", 15))
            if self.last_result_at and (time.time() - self.last_result_at > stale_after):
                self.dashboard.set_status("stale")

            if self.skip_similar and self.last_frame is not None and not is_meaningfully_different(self.last_frame, frame):
                append_jsonl(self.log_file, {
                    "event": "capture_skip_similar",
                    "capture_timestamp": capture_ts,
                    "status": "skipped",
                })
                self._sleep_until_next(cycle_start)
                continue

            self.last_frame = frame
            frame_path = str(save_frame(frame, self.snapshot_dir))
            self._enqueue_for_analysis(frame_path, capture_ts)
            self._sleep_until_next(cycle_start)

    def _enqueue_for_analysis(self, frame_path: str, capture_ts: str) -> None:
        with self.state_lock:
            should_start, _ = self.buffer.enqueue(frame_path)
            if not should_start:
                append_jsonl(self.log_file, {
                    "event": "analysis_enqueued_latest",
                    "frame_path": frame_path,
                    "capture_timestamp": capture_ts,
                    "status": "pending_overwrite",
                })
                return
            threading.Thread(target=self._run_analysis, args=(frame_path, capture_ts), daemon=True).start()

    def _run_analysis(self, frame_path: str, capture_ts: str) -> None:
        analysis_start = utc_timestamp()
        self.dashboard.set_status("analyzing")
        try:
            payload = self.analysis_client.analyze_image_with_optional_web_search(
                image_path=frame_path,
                system_prompt=self.system_prompt,
            )
            parsed = validate_analysis_payload(payload, self.schema_path)
            self.last_result_at = time.time()
            self.dashboard.set_result(
                timestamp=self.last_result_at,
                result=parsed,
                frame_path=frame_path,
            )
            self.dashboard.set_status("idle")
            append_jsonl(self.log_file, {
                "event": "analysis",
                "frame_path": frame_path,
                "capture_timestamp": capture_ts,
                "analysis_start_timestamp": analysis_start,
                "analysis_end_timestamp": utc_timestamp(),
                "status": "success",
                "parsed_response": parsed,
            })
        except Exception as exc:
            self.dashboard.set_error(str(exc))
            append_jsonl(self.log_file, {
                "event": "analysis",
                "frame_path": frame_path,
                "capture_timestamp": capture_ts,
                "analysis_start_timestamp": analysis_start,
                "analysis_end_timestamp": utc_timestamp(),
                "status": "error",
                "error": str(exc),
            })
        finally:
            with self.state_lock:
                next_frame = self.buffer.complete_and_pop_next()

            if next_frame:
                threading.Thread(target=self._run_analysis, args=(next_frame, utc_timestamp()), daemon=True).start()

    def _sleep_until_next(self, cycle_start: float) -> None:
        elapsed = time.time() - cycle_start
        time.sleep(max(0.0, self.capture_interval - elapsed))
