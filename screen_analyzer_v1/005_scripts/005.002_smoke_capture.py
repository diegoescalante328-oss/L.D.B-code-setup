from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

import cv2


SCRIPT_DIR = Path(__file__).resolve().parent
APP_DIR = SCRIPT_DIR.parent / "001_app"


def _load_attr(relative_path: str, attr: str):
    module_path = APP_DIR / relative_path
    spec = importlib.util.spec_from_file_location(f"dynamic_{module_path.stem}", module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load module at {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, attr)


CameraCapture = _load_attr("002.001_camera/002.001.001_frame_capture.py", "CameraCapture")
save_frame = _load_attr("002.001_camera/002.001.002_frame_utils.py", "save_frame")
parse_camera_source = _load_attr("002.001_camera/002.001.003_stream_sources.py", "parse_camera_source")


def main() -> None:
    parser = argparse.ArgumentParser(description="Open a camera source and save frames manually.")
    parser.add_argument("--source", default="0", help="Device index like 0 or a URL")
    parser.add_argument("--output-dir", default="008_outputs/smoke", help="Where to save captured frames")
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
