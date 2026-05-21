# QA Polish Patterns for Luxury Real-Estate Teasers

Use this reference when a generated/rendered teaser exists but should not be delivered until visual relevance and documentation pass.

## Common QA failure pattern

A render can be technically valid (16:9, audio present, logo outro present) but still fail luxury real-estate relevance. Do not deliver solely because files exist.

Typical failures to catch from contact sheets/sample frames:

- **Wrong material/craft shot:** quarry, mountain, raw outdoor stone, construction aggregate, or countryside stone visuals used where the intent was premium interior material/craftsmanship. Replace with marble/fabric/wood veneer/interior samples/artisan hands/bespoke furniture close-ups.
- **Wrong-city skyline:** generic North American/European skyline or non-Dubai towers used for a Dubai/SZR/Downtown/Jumeirah Garden City project. Replace with Burj Khalifa, Sheikh Zayed Road, Museum of the Future, Dubai Frame, Downtown/Business Bay, or credible Dubai high-rise/residential context.
- **Documentation gap:** final MP4s exist but `shot_plan.md`, `source_provenance.md`, or `audit_summary.md` are missing. Treat this as not delivery-ready for premium client work.

## Recommended polish sequence

1. Generate/contact-sheet sample frames at regular timestamps and inspect visually before sending media.
2. Identify shots that violate project facts or user exclusions by timestamp.
3. Patch only the weak segments if the rest of the edit is acceptable; do not restart the full edit unnecessarily.
4. Preserve exact user-supplied logo assets as overlays/outros; do not AI-redraw brand text.
5. Re-export both master and Telegram/social encode.
6. Re-run `ffprobe` or equivalent validation for dimensions, duration, codec, and audio.
7. Regenerate contact sheet/samples after fixes.
8. Write or update:
   - `notes/shot_plan.md` — final segment timing and role.
   - `notes/source_provenance.md` — URLs/license notes/source type and selected time ranges where available.
   - `notes/audit_summary.md` — checklist result and any honest limitations.
9. Deliver only after QA passes, not merely when the background service exits.
