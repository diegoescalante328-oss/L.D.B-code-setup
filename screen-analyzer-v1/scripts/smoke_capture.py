from __future__ import annotations

import argparse

import cv2

from app.camera.capture import CameraCapture
from app.camera.frame_utils import save_frame
from app.camera.stream_sources import parse_camera_source


def main() -> None:
    parser = argparse.ArgumentParser(description="Open a camera source and save frames manually.")
    parser.add_argument("--source", default="0", help="Device index like 0 or a URL")
    parser.add_argument("--output-dir", default="outputs/smoke", help="Where to save captured frames")
    args = parser.parse_args()

    capture = CameraCapture(source=parse_camera_source(args.source), startup_timeout_seconds=30)
    status = capture.connect()
    if not status.connected:
        raise RuntimeError(status.message)

    print("Connected. Press 's' to save frame, 'q' to quit")
    while True:
        ok, frame = capture.read()
        if not ok or frame is None:
            print("Frame read failed")
            break

        cv2.imshow("Smoke Capture", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("s"):
            path = save_frame(frame, args.output_dir, prefix="smoke")
            print(f"Saved frame to: {path}")
        elif key == ord("q"):
            break

    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
