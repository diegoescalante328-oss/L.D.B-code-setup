from __future__ import annotations

from dataclasses import dataclass


@dataclass
class LatestFrameBuffer:
    analysis_in_flight: bool = False
    pending_frame_path: str | None = None

    def enqueue(self, frame_path: str) -> tuple[bool, str]:
        if self.analysis_in_flight:
            self.pending_frame_path = frame_path
            return False, frame_path
        self.analysis_in_flight = True
        return True, frame_path

    def complete_and_pop_next(self) -> str | None:
        if self.pending_frame_path is None:
            self.analysis_in_flight = False
            return None
        next_frame = self.pending_frame_path
        self.pending_frame_path = None
        self.analysis_in_flight = True
        return next_frame
