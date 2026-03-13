# AGENTS.md

## Source of truth order
Read these files first, in this order:
1. README.md
2. config/settings.yaml
3. config/prompts.yaml
4. schemas/screen_analysis.schema.json
5. docs/architecture.md
6. docs/build_order.md

## Project mission
Implement Version 1 of Screen Analyzer as a desktop application that:
- ingests a live camera feed of a monitor
- captures frames automatically every N seconds
- sends selected frames to the OpenAI Responses API
- continuously shows the latest useful result in a local UI

## Hard V1 constraints
- no manual trigger required for runtime
- default capture interval: 3 seconds
- at most one analysis request in flight
- queue policy: latest-frame-wins
- visible UI error state within 5 seconds
- logging must make each cycle traceable

## Working rules
- prefer small, testable modules
- prefer explicit structured output contracts
- do not expand scope before the local webcam path is stable
- keep logs JSON serializable
- keep UI updates on the Tk main thread
