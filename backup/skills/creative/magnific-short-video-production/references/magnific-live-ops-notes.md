# Magnific Live Ops Notes

## Generation sequence
1. Verify Magnific login first.
2. Open Video Generator.
3. Inspect `Model -> All models`.
4. Pick the best Unlimited-capable model for the current shot.
5. Prepare/select clean reference frames first.
6. Verify the left form before every generate click:
   - model
   - Unlimited mode
   - aspect ratio
   - duration
   - clean start image
   - prompt matches shot ID
7. Queue clips in shot order.
8. If the current model is full, switch to another Unlimited model and continue.

## Reference-image rules
- Never reuse a start image with a visible screen, frame border, UI-looking inset, or picture-in-picture composition.
- Prefer a clean protagonist portrait/reference frame for continuity-heavy shorts.
- Re-check the actual `Start image` slot on the left panel, not just the gallery selection.

## Model fallback rule
- Default anime-friendly Unlimited choice: Kling 2.5.
- If Kling 2.5 is temporarily full, open `All models` and switch to another Unlimited-capable model instead of waiting indefinitely.
- Keep the shot plan intact when switching models.

## Project note template
- Clean reference chosen:
- Bad framed references to avoid:
- Primary model:
- Unlimited fallback model(s):
- Aspect ratio:
- Duration per clip:
- Queued clips:
- Completed downloads:
