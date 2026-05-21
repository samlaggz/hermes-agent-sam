# Anime shorts + Magnific notes

## Viral short-form pattern

A strong anime-style short usually has:
- a **hook in the first 1–2 seconds**
- one clear emotional premise or mystery
- very readable mobile-first framing
- 3–5 visual beats, not a long scene list
- a payoff or cliffhanger that invites rewatch / comments

## Discovery / SEO notes

Official YouTube guidance emphasizes that discovery is not just keywords. Stronger signals include:
- click decision when the video is shown
- average view duration
- average percent viewed
- viewer satisfaction / engagement
- personalization to the viewer

Practical lesson: shorts should optimize for **instant curiosity + retention**, not title stuffing.

## Title / thumbnail lessons from official YouTube guidance

- titles should be accurate and concise
- put important words early
- thumbnail and title should work together
- custom thumbnails matter heavily for broader video discovery

For shorts, the first frame often acts like the thumbnail-in-motion, so the opening image must be strong.

## Copyright safety notes

From YouTube copyright guidance, the safe route is to use:
- original characters
- original costume design
- original worldbuilding
- licensed or original music only

Avoid:
- direct recreation of famous anime characters
- exact costume copies
- franchise logos / symbols
- copied scenes or signature props
- copyrighted soundtrack use without rights

"Anime-inspired original IP" is safer than fan recreation.

## Magnific-specific workflow notes

- Before generating, downloading, or exporting anything, confirm Magnific auth state.
- If logged out, do Magnific login first using current-session credentials only.
- If Magnific throws a CAPTCHA on login, pause for manual completion in the live browser.
- Keep GUI/live browsing and non-GUI browser automation on the same shared CDP browser when possible.
- Structured JSON-style prompts work better than loose prompts for multi-scene consistency.

## Example structured prompt fields

```json
{
  "project": "viral_anime_short",
  "scene_id": "scene_1_hook",
  "shot_type": "vertical cinematic manga splash frame",
  "subject": "original anime-inspired protagonist",
  "action": "discovers an impossible threat",
  "setting": "neon city alley in rain",
  "style": {
    "medium": "manga-inspired anime illustration",
    "linework": "clean inked outlines",
    "rendering": "high-detail cel shading",
    "mood": "urgent cinematic"
  },
  "composition": {
    "aspect_ratio": "9:16",
    "camera": "low angle close-medium shot",
    "focus": "hero expression and reveal object"
  },
  "constraints": [
    "original IP only",
    "no copyrighted characters",
    "no logos",
    "no watermarks"
  ],
  "output": "high-detail key visual for short-form anime teaser"
}
```
