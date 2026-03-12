# Build Order

1. Set up the OpenAI API side
   - create API key
   - store it in environment variable
   - never hardcode secrets

2. Get the camera feed onto the laptop
   - prove the laptop can open the incoming feed reliably

3. Build the capture loop
   - open the source
   - display it
   - save a frame manually for debugging

4. Send one saved image to OpenAI
   - do not start with full live automation

5. Add automatic frame sampling
   - analyze every few seconds
   - or only when the scene changes

6. Build the side-by-side dashboard
   - live feed
   - latest answer
   - status indicators

7. Add optional web search
   - only when current info is actually needed

8. Add structure to the output
   - what the screen contains
   - whether there is a question
   - answer
   - citations
   - notes
