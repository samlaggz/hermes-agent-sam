# True-video Shorts workflow

Condensed from a Magnific anime-thriller session where the user rejected a hybrid slideshow/video result.

## Trigger
Use this workflow when the user asks for a Short/Reel/TikTok that must feel like a real edited video rather than animated stills.

## Required production order
1. Finalize concept and hook first.
2. Write the full scene list before generation.
3. For each scene, lock:
   - duration
   - aspect ratio (usually 9:16)
   - narrative beat
   - visual prompt
   - continuity anchors (same character traits, wardrobe, palette)
4. Generate each scene as a native Magnific video clip.
5. Download all clips.
6. Record/render the full voiceover.
7. Assemble in post with captions, pacing trims, and platform-safe encode settings.

## Hook heuristic
- First 1-3 seconds must contain the mystery, threat, contradiction, or reveal.
- Strong pattern: hook -> clue escalation -> reveal/twist -> cliffhanger/payoff.

## Character consistency anchors
Repeat the same compact identifiers in every prompt:
- eye color
- hair style
- signature clothing item
- mood/palette
- camera language

Example pattern:
"same Ren, amber eyes, black windswept hair, ink-stained fingers, dark school uniform, neon-rain noir palette"

## Anti-patterns to avoid
- Building most of the short from still images with motion effects.
- Generating clips before the full cut plan exists.
- Treating a rough prototype as the base for final polish when the workflow itself is wrong.
- Forgetting to verify Magnific login/session state before queueing generations.

## Good target shape
For a 45-90s short, plan ~5-8 clips of 5-10s each, then stitch and trim to narration timing.
