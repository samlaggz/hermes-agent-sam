# Brochure-driven luxury real-estate teaser workflow

Use this reference when the user uploads a developer brochure/PDF and asks for a premium project teaser using stock or generated footage.

## Key workflow

1. **Extract the brochure first**
   - Use PyMuPDF or the document extraction skill to pull text, page renders, and embedded images.
   - Save extracted text, first-page/logo candidates, and page renders in the project directory before launching long video work.
   - Pull durable facts from the brochure: developer/project name, tagline, location, skyline references, amenities, rarity/positioning, and design language.

2. **Turn brochure facts into a location/amenity shot bible**
   - Location must drive stock-footage selection. If the project says Jumeirah Garden City / Sheikh Zayed Road, prefer SZR, Downtown Dubai, Burj Khalifa, Dubai Frame, Museum of the Future, and nearby urban skyline cues.
   - Reject footage that shifts the project identity to unrelated villas, resorts, countryside, generic beaches, or random lifestyle scenes.
   - For residential luxury, prioritize: tower/building exteriors, skyline/balcony views, lobby/concierge, pool/rooftop, gym/wellness, landscaped podium, business lounge/co-working, furnished interiors.

3. **Respect negative visual constraints**
   - Do not show floor plans/unit plans when the user says not to.
   - Do not use watermarked previews or thumbnails as final footage.
   - Do not use brand website hero videos or brochure imagery as main footage unless explicitly allowed and license-safe; use brochure/website primarily for brand facts, logo, palette, and copy.
   - Keep the requested aspect ratio from the start. For landscape, build a clean 16:9 project, not a repurposed reel.

4. **Logo and outro discipline**
   - Extract exact logo art from the brochure when possible.
   - Preserve text/logo exactly in local motion graphics. If using Magnific for an outro, generate abstract/premium background motion only; do not let AI recreate or distort brand/logo text.

5. **Assembly expectations**
   - Use soothing premium music, beat-synced transitions, occasional tasteful black-screen cuts on beat, and a final color grade so mixed stock clips share one warm luxury palette.
   - Write provenance for every clip/source and license note.
   - Final audit should include ffprobe metadata plus visual frame sampling for watermark, wrong-location vibe, villas/floor plans, portrait wrappers, and color mismatch.

## Prompt skeleton for background workers

Include:
- source PDF path and extracted asset directory;
- workdir/final output paths;
- project facts extracted from brochure;
- approved/forbidden visual categories;
- stock-source policy: free/commercial-use/no-watermark only unless logged-in original downloads are available;
- logo extraction/outro instructions;
- music/editing/color/audit requirements;
- instruction to notify user immediately on blockers such as CAPTCHA, OTP, licensing gaps, or Magnific access issues.
