# Magnific Unlimited Video Model Notes

Durable notes from a real Magnific video-generation session focused on anime-style vertical shorts.

## Goal shape
- user wanted anime-inspired crime-thriller short-form video
- user explicitly wanted the **best Unlimited model** available in Magnific Video Generator
- user wanted a finished **45–90 second** short, not just a single clip

## Observed live model-list pattern
When the model list was opened in Magnific Video Generator, the app exposed a mix of premium and unlimited-capable options.

Observed useful entries included:
- Kling 2.5 — `Unlimited`, `Illustration & animation`, `Start / End`, `720p - 1080p`, `5 - 10s`
- MiniMax Hailuo 2.3 — `Unlimited`, but more realism-oriented
- MiniMax Hailuo 2.3 Fast — `Unlimited`, more realism-oriented
- Wan 2.2 — `Unlimited`, lower-resolution / different fit

## Best observed fit for anime-style unlimited work
For **anime / illustration-heavy short-form video**, the best observed Unlimited choice was:
- **Kling 2.5**

Reason:
- explicitly supports **Illustration & animation**
- available under **Unlimited**
- workable for `9:16` short-form
- better style fit than realism-first unlimited models

## Important limitation
Kling 2.5 in this workflow behaved like a **clip generator**, not a one-shot long-form story generator.

Observed practical consequence:
- the right workflow for a 45–90 second short was **multi-clip generation + local assembly**
- do not assume the app can output the whole finished story at requested long duration just because the model is "Unlimited"

## Entry-path lesson
A good way into the video tool was:
1. start from a good image result or anchor still
2. use the image card's **Create video** action
3. let that attach the still as the **Start image** in Video Generator
4. then switch model and settings

This produced a cleaner setup than trying to recreate everything manually from a blank video form.

## Unlimited-mode lesson
The app can show a state where the chosen model is valid but the current settings are **not yet in Unlimited mode**.

Observed pattern:
- after selecting Kling 2.5, Magnific warned that the current resolution was not supported by Unlimited
- clicking the in-app control to **Switch to Unlimited mode** changed the workflow to a valid unlimited state
- after that, the form showed the current resolution as covered by **Unlimited videos for this resolution**

## Practical generation shape used
- aspect ratio: `9:16`
- duration: `10s`
- prompt style: structured JSON-like prompt with `scene`, `character`, `setting`, `action`, `camera`, `mood`, `lighting`, `style`, `motion`, `negative`

## Final production lesson
When the user wants a complete short immediately:
- generate at least one real Magnific video clip and supporting Magnific assets
- keep the TTS separate
- if the model remains clip-limited, assemble the longer short locally from:
  - Magnific clip(s)
  - Magnific still assets
  - narration
  - editorial pacing / captions / music

This is a valid completion path when the user's real goal is the **finished short**, not proof that every second was created in one app render.
