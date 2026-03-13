# Screen Analyzer V1

Screen Analyzer V1 is a local desktop app that ingests an external camera feed of a monitor, captures frames automatically every few seconds, analyzes selected frames with the OpenAI Responses API (structured JSON), and continuously updates a local Tkinter dashboard.

## Implemented V1 behavior
- Autonomous capture loop (no manual analyze button required)
- Default capture interval = 3s, bounded to 2..10s by config validation
- One in-flight analysis request at a time
- Latest-frame-wins buffering when analysis is busy
- Optional skip of near-identical frames via simple frame difference
- UI status + error + latest result + result timestamp + live feed preview
- JSONL runtime logs for capture/analysis outcomes
- Camera source supports device index (`0`) or URL (`rtsp://...`, `http://...`)

## Requirements
- Python 3.11+
- OpenCV-compatible camera source (USB webcam index or URL stream)
- `OPENAI_API_KEY` environment variable

Install:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Set environment variables:

```bash
export OPENAI_API_KEY=your_key_here
```

## Runtime root
Use `screen_analyzer_v1/` as the canonical runtime root. Run commands from this directory.

Environment bootstrap guide: `011_env/011.001_virtual_environment_setup.md`.
Step-by-step setup and execution checklist: `007_docs/007.004_setup_and_run.md`.

## Configuration and schema locations
- Runtime config: `002_config/002.002_runtime_settings.yaml`
- Prompt config: `002_config/002.001_prompt_settings.yaml`
- Structured output schema: `003_schemas/003.001_screen_analysis_schema.json`

Edit `002_config/002.002_runtime_settings.yaml`.

Key fields:
- `camera.source`: `0` (device) or stream URL
- `capture.interval_seconds`: default `3`
- `capture.skip_similar_frames`: true/false
- `analysis.enable_web_search_second_pass`: optional second pass path
- `ui.stale_after_seconds`: marks status as stale when no fresh result

## Run commands
### 1) Smoke capture (camera connectivity)
```bash
python 005_scripts/005.002_smoke_capture.py --source 0 --output-dir 008_outputs/smoke
```
Press `s` to save a frame and `q` to quit.

### 2) Single-frame structured analysis
```bash
python 005_scripts/005.001_single_frame_analysis.py --image 008_outputs/smoke/<your_image>.jpg
```

### 3) Full desktop app
```bash
python 001_app/002_app_entrypoint.py
```

## Logs and outputs
- Saved frames: `008_outputs/snapshots/`
- Runtime logs: `010_logs/runtime.jsonl`

Each analysis record includes frame path, capture timestamp, analysis start/end timestamps, status, and either parsed response or error.

## Known V1 limitations
- Crop calibration is minimal (optional config scaffold only)
- No OCR-specific side pipeline
- No multi-camera orchestration
- No browser automation or input control features (out of scope)
