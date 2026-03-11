# Screen Analyzer V1

Version 1 is a laptop-side app that ingests a live external camera feed of a monitor, captures frames every N seconds, sends selected frames to an OpenAI vision pipeline, and continuously displays the latest useful analysis result without manual triggering.

## V1 defaults
- Capture interval: 3 seconds
- Allowed range: 2 to 10 seconds
- Max in-flight analysis requests: 1
- Queue policy: latest-frame-wins
- Minimum unattended runtime target: 60 minutes

## Core pipeline
Camera Device -> Video Feed to Laptop -> Laptop Capture Service -> Frame Sampler -> OpenAI Analysis Service -> Answer / Overlay UI

## Manual setup
1. Create and activate a virtual environment
2. Install requirements
3. Copy `.env.example` to `.env`
4. Put your OpenAI API key in `.env`
5. Adjust `config/settings.yaml`
6. Test the camera feed first with `scripts/smoke_capture.py`
7. Test one saved frame with `scripts/single_frame_analysis.py`

## Notes
- V1 is autonomous timed capture, not manual analyze button driven
- The camera source may be a device index or an IP stream URL
- Structured JSON output should be used from the beginning
