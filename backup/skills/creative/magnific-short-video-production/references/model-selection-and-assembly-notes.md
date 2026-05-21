# Model selection and assembly notes

## Magnific Video Generator observations

Observed useful model-picker entries during a live session included:
- Kling 2.5 — `Illustration & animation`, `Start / End`, `720p - 1080p`, `5 - 10s`, **Unlimited**
- Kling 2.1 — illustration-friendly but not the preferred choice once Kling 2.5 was available
- PixVerse 6 — illustration-friendly, but not selected as the primary recommendation for this workflow
- MiniMax Hailuo 2.3 / Fast — Unlimited, but oriented toward realistic video rather than anime-first output
- Wan 2.2 — Unlimited, but not the best fit for anime-style illustrated thriller shorts in this session

## Durable takeaway

When the user's priority is:
- anime / manga-inspired visual language,
- unlimited generation,
- vertical viral short production,

then **Kling 2.5** is the best first choice among the observed Unlimited options because it explicitly supports **Illustration & animation**.

## Important UI nuance

After selecting Kling 2.5, Magnific may show a message like:
- current resolution is not supported by Unlimited
- `Switch to Unlimited mode`

Use the built-in switch/link, then verify the panel reflects:
- compatible resolution (observed: `720`)
- vertical format if needed (`9:16`)
- `Unlimited` status before generating

## Assembly rule for 45–90 second shorts

Do not promise a one-shot long-form generation when using the best unlimited anime-capable model.

Instead:
1. plan 5–10 story beats,
2. generate 5–10 short clips,
3. download clips,
4. stitch them externally,
5. sync external narration.

## Andrew narration note

Observed reliable approach:
- use `en-US-AndrewNeural`
- split long scripts into chunks under ~260 chars
- render chunk MP3s
- concatenate with ffmpeg

This is more reliable than a single long request for thriller-length narration.
