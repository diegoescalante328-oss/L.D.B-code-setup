# Version 1 Acceptance Specification

## Objective
Version 1 is successful if it can:
- ingest a live camera feed of a monitor from an external device
- autonomously capture a frame every few seconds
- send frames to an LLM vision pipeline without manual triggering
- return a useful analysis to the laptop UI
- continue doing so unattended for a sustained period
- surface errors instead of failing silently

## Default runtime parameters
- Capture interval: 3s
- Allowed capture interval: 2 to 10s
- Max in-flight analysis requests: 1
- Queue policy: latest-frame-wins
- Minimum unattended runtime: 60m

## Functional acceptance criteria
- Live feed visible within 30 seconds of startup
- Timed capture starts automatically
- Analysis loop runs automatically
- Latest result panel shows timestamp, frame ID or capture time, response, status
- Errors are surfaced in UI within 5 seconds
- Logs include frame ID, timestamps, status, response or error

## Quality acceptance criteria
On 20 clear validation scenes:
- primary content identification >= 18/20
- prompt or question detection >= 18/20
- useful answer or summary >= 16/20

Freshness targets:
- median capture-to-display freshness <= 8s
- p95 freshness <= 15s

## Stability acceptance criteria
- 60-minute unattended run without crash, deadlock, silent stall, or required manual restart
- recovery within 15s after transient feed or network restoration if outage <= 30s

## Hard failure conditions
- no autonomous loop
- silent failure
- median freshness > 15s
- useful output rate < 80 percent on validation set
- unbounded queue or memory growth
- insufficient logs to diagnose failures
