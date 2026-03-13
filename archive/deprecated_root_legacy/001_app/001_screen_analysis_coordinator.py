from __future__ import annotations

import threading
import time
from pathlib import Path
from typing import Any, Optional

from app.analysis.openai_client import OpenAIAnalysisClient
from app.analysis.parser import validate_analysis_payload
from app.analysis.prompt_builder import build_system_prompt
from app.analysis.scene_change import is_meaningfully_different
from app.camera.capture import CameraStream
from app.camera.frame_utils import save_frame, utc_timestamp
from app.storage.logs import append_jsonl


class Coordinator:
    def __init__(
        self,
        dashboard: Any,
        camera_source: int | str = 0,
        capture_interval: int | float = 3,
        schema_path: str | Path = "schemas/screen_analysis.schema.json",
        snapshot_dir: str | Path = "outputs/snapshots",
        log_file: str | Path = "logs/runtime.jsonl",
        skip_similar_frames: bool = True,
    ) -> None:
        self.dashboard = dashboard
        self.camera_source = camera_source
        self.capture_interval = max(1.0, float(capture_interval))
        self.schema_path = Path(schema_path)
        self.snapshot_dir = Path(snapshot_dir)
        self.log_file = Path(log_file)
        self.skip_similar_frames = skip_similar_frames

        self.snapshot_dir.mkdir(parents=True, exist_ok=True)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        self.analysis_client = OpenAIAnalysisClient(schema_path=self.schema_path)
        self.system_prompt = build_system_prompt()
        self.camera = CameraStream(self.camera_source)

        self.worker_thread: Optional[threading.Thread] = None
        self.running = False
        self.last_frame = None
        self.pending_frame: Optional[Path] = None
        self.analysis_in_flight = False
        self.lock = threading.Lock()

    def start(self) -> None:
        self.dashboard.set_status("Connecting camera...")
        self.camera.open()
        self.running = True
        self.dashboard.set_status("Running")
        self.worker_thread = threading.Thread(target=self.loop, daemon=True)
        self.worker_thread.start()

    def stop(self) -> None:
        self.running = False
        self.camera.release()
        self.dashboard.set_status("Stopped")

    def loop(self) -> None:
        while self.running:
            cycle_start = time.time()

            ok, frame = self.camera.read()
            if not ok or frame is None:
                if not self.running:
                    break
                self.dashboard.set_status("Camera read failure")
                append_jsonl(
                    self.log_file,
                    {
                        "timestamp": utc_timestamp(),
                        "status": "error",
                        "error": "camera_read_failure",
                    },
                )
                time.sleep(1)
                continue

            self.dashboard.set_preview(frame)

            if self.skip_similar_frames and self.last_frame is not None:
                if not is_meaningfully_different(self.last_frame, frame):
                    self._sleep_remaining(cycle_start)
                    continue

            self.last_frame = frame.copy()

            try:
                frame_path = save_frame(frame, self.snapshot_dir)
            except Exception as exc:
                self.dashboard.set_status(f"Frame save error: {exc}")
                append_jsonl(
                    self.log_file,
                    {
                        "timestamp": utc_timestamp(),
                        "status": "error",
                        "error": f"frame_save_error: {exc}",
                    },
                )
                self._sleep_remaining(cycle_start)
                continue

            with self.lock:
                if self.analysis_in_flight:
                    self.pending_frame = frame_path
                else:
                    self.analysis_in_flight = True
                    threading.Thread(
                        target=self.run_analysis,
                        args=(frame_path,),
                        daemon=True,
                    ).start()

            self._sleep_remaining(cycle_start)

    def _sleep_remaining(self, cycle_start: float) -> None:
        elapsed = time.time() - cycle_start
        time.sleep(max(0.0, self.capture_interval - elapsed))

    def _format_result_text(self, result: dict[str, Any]) -> str:
        notes = result.get("notes", []) or []
        citations = result.get("citations", []) or []
        notes_block = "\n".join(f"- {note}" for note in notes) if notes else "- None"
        citations_block = "\n".join(f"- {citation}" for citation in citations) if citations else "- None"

        return (
            f"Screen content:\n{result['screen_content']}\n\n"
            f"Readability: {result['readability']}\n"
            f"Question present: {result['question_present']}\n"
            f"Needs web search: {result['needs_web_search']}\n\n"
            f"Main answer:\n{result['main_answer']}\n\n"
            f"Summary:\n{result['summary']}\n\n"
            f"Notes:\n{notes_block}\n\n"
            f"Citations:\n{citations_block}"
        )

    def run_analysis(self, frame_path: Path) -> None:
        started_at = time.time()
        timestamp = utc_timestamp()

        try:
            if not self.running:
                return

            self.dashboard.set_status("Analyzing...")
            result = self.analysis_client.analyze_image_with_optional_web_search(
                image_path=frame_path,
                system_prompt=self.system_prompt,
            )
            validate_analysis_payload(result, self.schema_path)
            formatted = self._format_result_text(result)

            if self.running:
                self.dashboard.set_result(timestamp, formatted)
                self.dashboard.set_status("Running")

            append_jsonl(
                self.log_file,
                {
                    "timestamp": timestamp,
                    "frame": str(frame_path),
                    "status": "success",
                    "analysis_duration_seconds": round(time.time() - started_at, 3),
                    "result": result,
                },
            )
        except Exception as exc:
            if self.running:
                self.dashboard.set_status(f"Error: {exc}")
                self.dashboard.set_result(timestamp, f"Analysis failed:\n{exc}")

            append_jsonl(
                self.log_file,
                {
                    "timestamp": timestamp,
                    "frame": str(frame_path),
                    "status": "error",
                    "analysis_duration_seconds": round(time.time() - started_at, 3),
                    "error": str(exc),
                },
            )
        finally:
            with self.lock:
                if not self.running:
                    self.analysis_in_flight = False
                    self.pending_frame = None
                    return

                if self.pending_frame is not None:
                    next_frame = self.pending_frame
                    self.pending_frame = None
                    threading.Thread(
                        target=self.run_analysis,
                        args=(next_frame,),
                        daemon=True,
                    ).start()
                else:
                    self.analysis_in_flight = False
