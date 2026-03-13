from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional

import cv2
from PIL import Image, ImageTk


class Dashboard:
    def __init__(self, title: str = "Screen Analyzer V1") -> None:
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry("1100x760")
        self.root.minsize(900, 650)

        self.on_close_callback: Optional[Callable[[], None]] = None
        self._preview_photo: Optional[ImageTk.PhotoImage] = None

        self.status_var = tk.StringVar(value="Idle")
        self.timestamp_var = tk.StringVar(value="No result yet")

        self.root.protocol("WM_DELETE_WINDOW", self._handle_close)
        self._build_layout()

    def _build_layout(self) -> None:
        top = ttk.Frame(self.root, padding=10)
        top.pack(fill="x")

        ttk.Label(top, text="Status:").pack(side="left")
        ttk.Label(top, textvariable=self.status_var).pack(side="left", padx=(5, 20))
        ttk.Label(top, text="Latest Result Time:").pack(side="left")
        ttk.Label(top, textvariable=self.timestamp_var).pack(side="left", padx=(5, 0))

        body = ttk.Frame(self.root, padding=10)
        body.pack(fill="both", expand=True)
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        left = ttk.LabelFrame(body, text="Live Preview", padding=10)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        left.rowconfigure(0, weight=1)
        left.columnconfigure(0, weight=1)

        self.feed_label = ttk.Label(left, text="Waiting for camera frames...", anchor="center")
        self.feed_label.grid(row=0, column=0, sticky="nsew")

        right = ttk.LabelFrame(body, text="Latest Analysis", padding=10)
        right.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        right.rowconfigure(0, weight=1)
        right.columnconfigure(0, weight=1)

        self.result_text = tk.Text(right, wrap="word")
        self.result_text.grid(row=0, column=0, sticky="nsew")
        self.result_text.insert("1.0", "Waiting for analysis...")
        self.result_text.configure(state="disabled")

        scrollbar = ttk.Scrollbar(right, orient="vertical", command=self.result_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.result_text.configure(yscrollcommand=scrollbar.set)

    def set_on_close(self, callback: Callable[[], None]) -> None:
        self.on_close_callback = callback

    def _handle_close(self) -> None:
        if self.on_close_callback is not None:
            try:
                self.on_close_callback()
            except Exception:
                pass
        self.root.destroy()

    def set_status(self, text: str) -> None:
        self.root.after(0, self._set_status_on_main_thread, text)

    def _set_status_on_main_thread(self, text: str) -> None:
        if self.root.winfo_exists():
            self.status_var.set(text)

    def set_result(self, timestamp: str, result_text: str) -> None:
        self.root.after(0, self._set_result_on_main_thread, timestamp, result_text)

    def _set_result_on_main_thread(self, timestamp: str, result_text: str) -> None:
        if not self.root.winfo_exists():
            return
        self.timestamp_var.set(timestamp)
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", result_text)
        self.result_text.configure(state="disabled")

    def set_preview(self, frame) -> None:
        if frame is None:
            return
        preview = frame.copy()
        self.root.after(0, self._set_preview_on_main_thread, preview)

    def _set_preview_on_main_thread(self, frame) -> None:
        if not self.root.winfo_exists():
            return

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(rgb)
        image.thumbnail((520, 360))
        self._preview_photo = ImageTk.PhotoImage(image=image)
        self.feed_label.configure(image=self._preview_photo, text="")

    def run(self) -> None:
        self.root.mainloop()
