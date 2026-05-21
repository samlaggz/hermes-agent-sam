# Magnific Unlimited and Queue Rules

Session-tested operating rules for short-video production in Magnific.

## Approved video-model pool for this workflow
Use only:
- Kling 2.5
- MiniMax Hailuo 2.3 Fast
- MiniMax Hailuo 2.3

Do not broaden the model pool unless the user changes the instruction.

## Required production order
1. Reset/discard stale project outputs if starting a new concept.
2. Write the script and cut plan first.
3. Generate clean reference images for the needed cuts.
4. Convert a clean image into the video Start image.
5. Verify all settings.
6. Submit video generation.
7. While a video is rendering or queued, prepare the next image prompt/reference.

## Unlimited verification rule
Immediately before every Generate click, verify the button itself visibly reads like:
- `Generate`
- `Unlimited`

This is stronger than checking nearby helper text alone.

## Kling 2.5 specific checks
- After selecting Kling 2.5, re-check resolution.
- If the UI lands on a priced/non-Unlimited resolution, lower it to an Unlimited-supported one before clicking Generate.
- A valid ready-to-submit state observed in session was:
  - Model: Kling 2.5
  - Resolution: 720
  - Duration: 10s
  - Aspect: 9:16
  - Start image present
  - Button text: `Generate / Unlimited`

## Capacity handling
- If Magnific shows a wait estimate for the current approved model, wait that amount and retry.
- If the model reports temporary full capacity without a useful estimate, retry after a short delay, still staying inside the approved model pool.
- Only switch among the approved video models for this user workflow.

## Image-to-video handoff
When using an image card's `Create video` action:
- confirm the navigation really lands in Video Generator
- confirm the selected image is populated in the Start image slot
- only then replace the prompt and submit the video
