from __future__ import annotations

import argparse
from pathlib import Path

import cv2

from app.camera.capture import CameraStream
from app.camera.frame_utils import save_frame
from app.camera.stream_sources import parse_camera_source


def main() -> None:
    parser = argparse.ArgumentParser(description="Smoke test camera capture.")
    parser.add_argument("--source", default="0", help="Camera source index or stream URL")
    parser.add_argument("--output-dir", default="outputs/smoke", help="Directory for saved test frames")
    args = parser.parse_args()

    source = parse_camera_source(args.source)
    camera = CameraStream(source)
    camera.open()

    print("Press 's' to save a frame, or 'q' to quit.")

    try:
        while True:
            ok, frame = camera.read()
            if not ok or frame is None:
                print("Camera read failure")
                break

            cv2.imshow("Smoke Capture", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("s"):
                path = save_frame(frame, Path(args.output_dir), prefix="smoke")
                print(f"Saved {path}")
            elif key == ord("q"):
                break
    finally:
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
