from __future__ import annotations

import threading
import time
from pathlib import Path
from typing import Optional

import cv2

from app.analysis.openai_client import OpenAIAnalysisClient
from app.analysis.parser import validate_analysis_payload
from app.analysis.scene_change import is_meaningfully_different
from app.camera.frame_utils import save_frame, utc_timestamp
from app.storage.logs import append_jsonl


class Coordinator:
    """
    Core runtime loop for Screen Analyzer.

    Responsibilities:
    - open camera
    - capture frames every N seconds
    - skip near-identical frames
    - enforce one in-flight request
    - latest-frame-wins buffering
    - update UI
    - write logs
    """

    def __init__(
        self,
        dashboard,
        camera_source=0,
        capture_interval=3,
        snapshot_dir="outputs/snapshots",
        log_file="logs/runtime.jsonl",
    ):
        self.dashboard = dashboard
        self.camera_source = camera_source
        self.capture_interval = capture_interval

        self.snapshot_dir = Path(snapshot_dir)
        self.log_file = Path(log_file)

        self.analysis_client = OpenAIAnalysisClient()

        self.cap = None

        self.running = False

        self.last_frame = None
        self.pending_frame = None

        self.analysis_in_flight = False

        self.lock = threading.Lock()

    def start(self):
        self.dashboard.set_status("Connecting camera")

        self.cap = cv2.VideoCapture(self.camera_source)

        if not self.cap.isOpened():
            raise RuntimeError("Camera could not be opened")

        self.running = True

        self.dashboard.set_status("Running")

        thread = threading.Thread(target=self.loop, daemon=True)
        thread.start()

    def loop(self):

        while self.running:

            start = time.time()

            ok, frame = self.cap.read()

            if not ok:
                self.dashboard.set_status("Camera read failure")
                time.sleep(1)
                continue

            if self.last_frame is not None:
                if not is_meaningfully_different(self.last_frame, frame):
                    time.sleep(self.capture_interval)
                    continue

            self.last_frame = frame

            frame_path = save_frame(frame, self.snapshot_dir)

            with self.lock:

                if self.analysis_in_flight:
                    # latest frame wins
                    self.pending_frame = frame_path
                else:
                    self.analysis_in_flight = True
                    threading.Thread(
                        target=self.run_analysis,
                        args=(frame_path,),
                        daemon=True,
                    ).start()

            elapsed = time.time() - start

            sleep_time = max(0, self.capture_interval - elapsed)
            time.sleep(sleep_time)

    def run_analysis(self, frame_path):

        timestamp = utc_timestamp()

        try:

            result = self.analysis_client.analyze_image_with_optional_web_search(
                image_path=frame_path,
                system_prompt="Analyze the monitor image."
            )

            validate_analysis_payload(result, "schemas/screen_analysis.schema.json")

            text = (
                f"Screen content:\n{result['screen_content']}\n\n"
                f"Answer:\n{result['main_answer']}\n\n"
                f"Summary:\n{result['summary']}"
            )

            self.dashboard.set_result(timestamp, text)

            append_jsonl(
                self.log_file,
                {
                    "timestamp": timestamp,
                    "frame": str(frame_path),
                    "status": "success",
                    "result": result,
                },
            )

        except Exception as e:

            self.dashboard.set_status(f"Error: {e}")

            append_jsonl(
                self.log_file,
                {
                    "timestamp": timestamp,
                    "frame": str(frame_path),
                    "status": "error",
                    "error": str(e),
                },
            )

        finally:

            with self.lock:

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
