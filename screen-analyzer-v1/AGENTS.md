# AGENTS.md

## Source of truth order
Read these files first, in this order:
1. README.md
2. docs/v1_acceptance_spec.md
3. docs/architecture.md
4. docs/build_order.md
5. docs/repo_structure.md
6. config/settings.yaml
7. config/prompts.yaml
8. schemas/screen_analysis.schema.json

## Project mission
Implement Version 1 of Screen Analyzer as a desktop application that:
- ingests a live external camera feed of a monitor
- captures frames automatically every N seconds
- sends selected frames to the OpenAI Responses API
- continuously shows the latest useful result in a local UI

## Hard V1 constraints
- no manual trigger required for real V1 runtime
- default capture interval: 3 seconds
- allowed capture interval: 2 to 10 seconds
- at most one analysis request in flight
- queue policy: latest-frame-wins
- UI must show feed, latest result, timestamp, status, and errors
- visible UI error state within 5 seconds
- support a 60-minute unattended run target
- logging must make each cycle traceable

## Out of scope
- browser automation
- mouse and keyboard control
- voice features
- OCR-specific side pipeline
- multi-camera
- multi-monitor
- autonomous browser navigation

## Implementation priorities
1. Config loading
2. Camera ingestion
3. Smoke capture
4. Single-frame analysis
5. Structured parsing
6. Bounded request policy
7. Desktop UI
8. Coordinator loop
9. Logging
10. Recovery behavior
11. Tests
