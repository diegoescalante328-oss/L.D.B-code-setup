from __future__ import annotations

import queue
import time
import tkinter as tk
from tkinter import ttk

import cv2
from PIL import Image, ImageTk

from app.camera.frame_utils import resize_for_preview
from app.ui.panels import format_result_payload


class Dashboard:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Screen Analyzer V1")
        self.root.geometry("1100x760")

        self.status_var = tk.StringVar(value="idle")
        self.timestamp_var = tk.StringVar(value="No result yet")
        self.error_var = tk.StringVar(value="")

        self.event_queue: queue.Queue[tuple[str, object]] = queue.Queue()
        self._feed_image = None

        self._build_layout()
        self.root.after(100, self._drain_events)

    def _build_layout(self) -> None:
        top = ttk.Frame(self.root, padding=10)
        top.pack(fill="x")

        ttk.Label(top, text="Status:").pack(side="left")
        ttk.Label(top, textvariable=self.status_var).pack(side="left", padx=(4, 20))

        ttk.Label(top, text="Latest Result:").pack(side="left")
        ttk.Label(top, textvariable=self.timestamp_var).pack(side="left", padx=(4, 20))

        ttk.Label(top, text="Error:").pack(side="left")
        ttk.Label(top, textvariable=self.error_var, foreground="red").pack(side="left", padx=(4, 0))

        body = ttk.Panedwindow(self.root, orient=tk.HORIZONTAL)
        body.pack(fill="both", expand=True, padx=10, pady=10)

        left = ttk.Frame(body)
        right = ttk.Frame(body)
        body.add(left, weight=1)
        body.add(right, weight=1)

        ttk.Label(left, text="Live Feed").pack(anchor="w")
        self.feed_label = ttk.Label(left, text="Waiting for camera...")
        self.feed_label.pack(fill="both", expand=True)

        ttk.Label(right, text="Latest Analysis").pack(anchor="w")
        self.result_text = tk.Text(right, wrap="word", height=35)
        self.result_text.pack(fill="both", expand=True)
        self.result_text.insert("1.0", "Waiting for analysis...")
        self.result_text.configure(state="disabled")

    def set_status(self, status: str) -> None:
        self.event_queue.put(("status", status))

    def set_error(self, error: str) -> None:
        self.event_queue.put(("error", error))

    def update_feed(self, frame) -> None:
        self.event_queue.put(("feed", frame))

    def set_result(self, timestamp: float, result: dict, frame_path: str) -> None:
        ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
        text = f"Frame: {frame_path}\n{format_result_payload(result)}"
        self.event_queue.put(("result", (ts, text)))

    def _drain_events(self) -> None:
        while True:
            try:
                event_type, value = self.event_queue.get_nowait()
            except queue.Empty:
                break

            if event_type == "status":
                self.status_var.set(str(value))
                if value != "error":
                    self.error_var.set("")
            elif event_type == "error":
                self.status_var.set("error")
                self.error_var.set(str(value))
            elif event_type == "result":
                ts, text = value
                self.timestamp_var.set(ts)
                self.result_text.configure(state="normal")
                self.result_text.delete("1.0", "end")
                self.result_text.insert("1.0", text)
                self.result_text.configure(state="disabled")
            elif event_type == "feed":
                frame = resize_for_preview(value)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(rgb)
                self._feed_image = ImageTk.PhotoImage(image=image)
                self.feed_label.configure(image=self._feed_image, text="")

        self.root.after(100, self._drain_events)

    def run(self) -> None:
        self.root.mainloop()
