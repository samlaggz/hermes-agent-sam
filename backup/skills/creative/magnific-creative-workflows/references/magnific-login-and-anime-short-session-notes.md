# Magnific login + anime short session notes

Condensed durable notes from a successful Magnific creative session.

## Login workflow that worked

- Best results came from a shared live Chromium session exposed over noVNC while Hermes browser tools attached to the same browser via CDP.
- Before any generation or download, check whether Magnific is already authenticated on the exact `/app/...` surface being used.
- If not authenticated:
  1. open the Magnific login flow in the shared session
  2. complete email/password
  3. if CAPTCHA appears, pause for manual solve in the live browser
  4. if Magnific asks for a 6-digit email code, enter the fresh OTP in the same session
  5. after success, return to the target generator page and verify logged-in app controls are visible

## Why this matters

Generation pages can lose editor state during auth redirects. After login, re-open the target tool and re-inject the prompt before generating.

## Prompting pattern that held up well

A structured prompt payload worked better than a loose prompt for multi-scene anime-inspired outputs. Useful fields:

- `project`
- `scene_id`
- `shot_type`
- `subject`
- `action`
- `setting`
- `style`
- `composition`
- `constraints`
- `output`

## Anime short recipe

- use original anime-inspired characters only
- vertical `9:16`
- 3 to 5 key images for the whole short
- first beat should work as a hook in ~1–2 seconds
- use captions and a cliffhanger or CTA at the end

## Asset workflow

- generate images in Magnific
- extract preview image URLs from the logged-in page state
- download selected images locally
- create a quick contact sheet to inspect coherence before editing
- animate stills into short vertical clips with motion/crop
- add narration and burned subtitles
- export a phone-safe MP4

## Export note

A first render can come out as `yuvj420p`; if strict compatibility is required, perform a final H.264 MP4 re-encode targeting `yuv420p` and `+faststart`.
