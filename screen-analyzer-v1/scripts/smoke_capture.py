from __future__ import annotations

import argparse

import cv2

from app.camera.frame_utils import save_frame
from app.camera.stream_sources import parse_camera_source


def main() -> None:
    parser = argparse.ArgumentParser(description="Open a camera source and save frames manually.")
    parser.add_argument("--source", default="0", help="Device index like 0 or a URL")
    parser.add_argument("--output-dir", default="outputs/smoke", help="Where to save captured frames")
    args = parser.parse_args()

    source = parse_camera_source(args.source)
    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        raise RuntimeError(f"Could not open camera source: {source}")

    print("Press 's' to save a frame.")
    print("Press 'q' to quit.")

    while True:
        ok, frame = cap.read()
        if not ok:
            print("Failed to read frame.")
            break

        cv2.imshow("Smoke Capture", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("s"):
            path = save_frame(frame, args.output_dir, prefix="smoke")
            print(f"Saved frame to: {path}")

        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()