from __future__ import annotations

import importlib.util
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


def _load_attr(relative_path: str, attr: str):
    module_path = Path(__file__).resolve().parent / relative_path
    spec = importlib.util.spec_from_file_location(f"dynamic_{module_path.stem}", module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load module at {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, attr)


OpenAIAnalysisClient = _load_attr("001.000_analysis/001.000.000_openai_client.py", "OpenAIAnalysisClient")
validate_analysis_payload = _load_attr("001.000_analysis/001.000.001_response_parser.py", "validate_analysis_payload")
load_system_prompt = _load_attr("001.000_analysis/001.000.002_prompt_builder.py", "load_system_prompt")
is_meaningfully_different = _load_attr("001.000_analysis/001.000.003_scene_change_detector.py", "is_meaningfully_different")
CameraCapture = _load_attr("002.001_camera/002.001.001_frame_capture.py", "CameraCapture")
parse_camera_source = _load_attr("002.001_camera/002.001.003_stream_sources.py", "parse_camera_source")
camera_utils = {
    "crop_frame": _load_attr("002.001_camera/002.001.002_frame_utils.py", "crop_frame"),
    "save_frame": _load_attr("002.001_camera/002.001.002_frame_utils.py", "save_frame"),
    "utc_timestamp": _load_attr("002.001_camera/002.001.002_frame_utils.py", "utc_timestamp"),
}
append_jsonl = _load_attr("003.002_storage/003.002.001_jsonl_logger.py", "append_jsonl")

crop_frame = camera_utils["crop_frame"]
save_frame = camera_utils["save_frame"]
utc_timestamp = camera_utils["utc_timestamp"]


@dataclass
class LatestFrameBuffer:
    """Single-slot queue implementing latest-frame-wins semantics."""

    analysis_in_flight: bool = False
    pending_frame: dict[str, str] | None = None

    def enqueue(self, frame_path: str, capture_ts: str) -> tuple[bool, dict[str, str]]:
        payload = {
            "frame_path": frame_path,
            "capture_ts": capture_ts,
        }
        if self.analysis_in_flight:
            self.pending_frame = payload
            return False, payload
        self.analysis_in_flight = True
        return True, payload

    def complete_and_pop_next(self) -> dict[str, str] | None:
        if self.pending_frame is None:
            self.analysis_in_flight = False
            return None
        next_frame = self.pending_frame
        self.pending_frame = None
        self.analysis_in_flight = True
        return next_frame


class Coordinator:
    def __init__(self, dashboard, settings: dict[str, Any], schema_path: str = "003_schemas/003.001_screen_analysis_schema.json") -> None:
        self.dashboard = dashboard
        self.settings = settings
        self.schema_path = schema_path

        camera_cfg = settings["camera"]
        capture_cfg = settings["capture"]
        app_cfg = settings["app"]
        recovery_cfg = settings["recovery"]

        self.capture_interval = float(capture_cfg["interval_seconds"])
        self.skip_similar = bool(capture_cfg.get("skip_similar_frames", True))
        self.latest_frame_wins = capture_cfg.get("latest_frame_wins") is True
        if not self.latest_frame_wins:
            raise ValueError("Coordinator requires capture.latest_frame_wins == true for V1")

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
            enable_web_search_second_pass=settings["analysis"].get("enable_web_search_second_pass", True),
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
        cycle_id = 0
        while self.running:
            cycle_id += 1
            cycle_start = time.time()
            capture_ts = utc_timestamp()
            ok, frame = self.camera.read()
            if not ok or frame is None:
                append_jsonl(self.log_file, {
                    "event": "camera_read_failed",
                    "capture_timestamp": capture_ts,
                    "status": "error",
                    "cycle_id": cycle_id,
                })
                self.dashboard.set_error("camera read failure; reconnecting")

                append_jsonl(self.log_file, {
                    "event": "camera_reconnect_started",
                    "capture_timestamp": capture_ts,
                    "status": "attempting",
                    "cycle_id": cycle_id,
                })
                reconnect_status = self.camera.reconnect()
                if reconnect_status.connected:
                    append_jsonl(self.log_file, {
                        "event": "camera_reconnect_succeeded",
                        "capture_timestamp": capture_ts,
                        "status": "success",
                        "cycle_id": cycle_id,
                    })
                    self.dashboard.set_status("idle")
                else:
                    append_jsonl(self.log_file, {
                        "event": "camera_reconnect_failed",
                        "capture_timestamp": capture_ts,
                        "status": "error",
                        "cycle_id": cycle_id,
                    })
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
                    "cycle_id": cycle_id,
                })
                self._sleep_until_next(cycle_start)
                continue

            self.last_frame = frame
            frame_path = str(save_frame(frame, self.snapshot_dir))
            self._enqueue_for_analysis(frame_path, capture_ts)
            self._sleep_until_next(cycle_start)

    def _enqueue_for_analysis(self, frame_path: str, capture_ts: str) -> None:
        with self.state_lock:
            should_start, payload = self.buffer.enqueue(frame_path, capture_ts)
            if not should_start:
                append_jsonl(self.log_file, {
                    "event": "analysis_enqueued_latest",
                    "frame_path": payload["frame_path"],
                    "capture_timestamp": payload["capture_ts"],
                    "status": "pending_overwrite",
                })
                return
            threading.Thread(target=self._run_analysis, args=(payload["frame_path"], payload["capture_ts"]), daemon=True).start()

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
                threading.Thread(
                    target=self._run_analysis,
                    args=(next_frame["frame_path"], next_frame["capture_ts"]),
                    daemon=True,
                ).start()

    def _sleep_until_next(self, cycle_start: float) -> None:
        elapsed = time.time() - cycle_start
        time.sleep(max(0.0, self.capture_interval - elapsed))
