# Architecture

## Core idea
Your proof of concept should be a 4-layer pipeline:

Layer 1: Capture  
A phone or iPad camera points at the monitor and produces a live feed.

Layer 2: Transport  
That feed gets from the mobile device to the laptop, either as a webcam-style source or an IP/RTSP stream.

Layer 3: Analysis  
The laptop samples frames from the feed and sends selected images to the OpenAI API for interpretation.

Layer 4: Display  
The laptop shows the live feed and the model's answer side by side.

## Expanded pipeline
Camera Device (iPad or phone)
-> Video Feed to Laptop
-> Laptop Capture Service
-> Frame Sampler
-> OpenAI Analysis Service
-> Answer / Overlay UI

## V1 note
Treat the camera device as dumb input hardware. AI runs on the laptop side.
