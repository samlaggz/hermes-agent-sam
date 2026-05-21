# Branded real-estate landscape videos: no-watermark recovery

Use this note when a user rejects a Magnific-made branded promo because the output used preview/watermarked media, wrong aspect ratio, weak music, or irrelevant stock footage.

## Trigger signals
- User says the video has a Magnific/Freepik/stock watermark.
- User says to log in to Magnific and use high-quality video.
- User says the output should be landscape, not reel/portrait.
- User rejects generic clips as unrelated to the brand location or amenities.

## Recovery workflow
1. Treat the prior output as rejected; do not salvage watermarked preview clips.
2. Verify the logged-in Magnific account before generating or downloading.
3. If OTP, CAPTCHA, or anti-bot/manual verification appears, stop and ask the user for the needed action; do not bypass it.
4. Start a clean versioned work directory and prompt that explicitly says:
   - no stock search previews, thumbnails, or preview MP4s as final footage;
   - only clean generated exports, logged-in originals, or licensed stock original downloads;
   - final format is 16:9 landscape, preferably 1920x1080;
   - delivery copy must also stay 16:9.
5. For branded real-estate content, lock location and amenities in the shot plan before sourcing footage. For Neoterra-style Dubai promos, include Dubai skyline/waterfront, beachfront/resort lifestyle, sports car/premium arrival, gym, swimming pool, and infinity pool.
6. Use the brand website only for logo/copy/tone unless the user explicitly allows website footage. Keep the official logo exact; do not AI-generate distorted logos.
7. Upgrade music as a production requirement, not an afterthought: use premium instrumental luxury real-estate style, refined lounge/deep-house/cinematic corporate bed, no voiceover unless requested.

## Verification checklist before delivery
- `ffprobe` confirms master and Telegram copy are 16:9 landscape.
- Every clip source is documented as generated original, licensed/original download, or local motion graphics.
- Visual inspection confirms no Magnific/Freepik/preview watermark remains.
- Audit summary confirms no brand-site footage was used except exact logo outro if allowed.
- The final response sends the actual media file when the platform supports it, not only a filesystem path.
