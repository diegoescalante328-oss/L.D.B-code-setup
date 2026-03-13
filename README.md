# Screen Analyzer V1

A local desktop app that captures frames from a camera source, analyzes meaningful screen changes with the OpenAI Responses API, and shows the latest structured result in a Tkinter dashboard.

## What V1 does
- Opens a camera source from device index or URL
- Captures frames every few seconds
- Skips near-identical frames
- Keeps at most one analysis request in flight
- Uses latest-frame-wins buffering when analysis is busy
- Shows status, latest result time, latest analysis text, and a live preview
- Writes runtime logs to JSONL
- Saves captured frames to `outputs/snapshots/`

## Quick start
Create a virtual environment and install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` from `.env.example` and set your API key.

Run the app:

```bash
python -m app.main
```

## Useful commands
Smoke test the camera:

```bash
python scripts/smoke_capture.py --source 0 --output-dir outputs/smoke
```

Analyze a single saved frame:

```bash
python scripts/single_frame_analysis.py --image outputs/smoke/your_image.jpg
```

## Repo map
- `app/analysis/` model calls, schema validation, scene change logic
- `app/camera/` camera helpers and stream source parsing
- `app/storage/` logs and snapshot persistence
- `app/ui/` Tkinter dashboard
- `config/` runtime settings and prompt config
- `schemas/` structured output schema
- `scripts/` smoke tests and one-off utilities

## Current V1 assumptions
- Run from the repo root with `python -m app.main`
- A local webcam is the easiest first camera source
- Network streams can be used if OpenCV can open them
