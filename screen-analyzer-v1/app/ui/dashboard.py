from __future__ import annotations

import tkinter as tk
from tkinter import ttk


class Dashboard:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Screen Analyzer V1")
        self.root.geometry("1000x700")

        self.status_var = tk.StringVar(value="Idle")
        self.timestamp_var = tk.StringVar(value="No result yet")
        self.result_var = tk.StringVar(value="Waiting for analysis...")

        top = ttk.Frame(self.root, padding=10)
        top.pack(fill="x")

        ttk.Label(top, text="Status:").pack(side="left")
        ttk.Label(top, textvariable=self.status_var).pack(side="left", padx=(5, 20))

        ttk.Label(top, text="Latest Result Time:").pack(side="left")
        ttk.Label(top, textvariable=self.timestamp_var).pack(side="left", padx=(5, 0))

        main = ttk.Frame(self.root, padding=10)
        main.pack(fill="both", expand=True)

        self.feed_label = ttk.Label(main, text="Live feed preview not wired yet")
        self.feed_label.pack(fill="x", pady=(0, 15))

        ttk.Label(main, text="Latest Analysis").pack(anchor="w")

        self.result_text = tk.Text(main, wrap="word", height=25)
        self.result_text.pack(fill="both", expand=True)
        self.result_text.insert("1.0", "Waiting for analysis...")
        self.result_text.configure(state="disabled")

    def set_status(self, text: str) -> None:
        self.status_var.set(text)
        self.root.update_idletasks()

    def set_result(self, timestamp: str, result_text: str) -> None:
        self.timestamp_var.set(timestamp)
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", result_text)
        self.result_text.configure(state="disabled")
        self.root.update_idletasks()

    def run(self) -> None:
        self.root.mainloop()