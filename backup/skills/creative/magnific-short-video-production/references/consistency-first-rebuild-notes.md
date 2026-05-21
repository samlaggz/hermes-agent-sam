# Consistency-first rebuild notes

Use when a user rejects a Magnific/AI-video short for character drift, scene drift, fake vertical framing, or dead-air pacing.

## Why prompt-only continuity failed

Session research and production experience showed a durable pattern:

- Most AI video systems do not maintain persistent character memory across separate generated clips.
- Text prompts alone can still reinterpret face, age, hair, wardrobe, or body proportions between clips.
- Lighting, camera angle, background changes, and scene changes all influence how the model reconstructs the subject.
- When identity drift appears, the next fix is usually reference structure, not just longer prompts.

## Corrective workflow

1. Treat the rejected cut as obsolete unless only one isolated clip is bad.
2. Build a short character bible before regenerating:
   - age range
   - face shape
   - skin tone
   - hair color/style
   - outfit silhouette
   - distinctive markers
   - recurring props
3. Build a scene/geography bible:
   - fixed room layout
   - door/window/threshold positions
   - palette and lighting logic
   - recurring props and surfaces
4. Generate or select clean reference images first:
   - one reusable protagonist reference
   - one reusable environment/reference frame when possible
   - reject nested frames, screen-within-screen, wrong outfit, wrong face, bad composition, or landscape-looking references
5. Use image/start-reference video generation for continuity-heavy clips.
6. Keep scenes near the same geography unless a location change is essential.
7. Prefer fewer, shorter clips when continuity is the priority.
8. Repeat the exact character and scene bible wording in every clip prompt.
9. Audit each generated clip immediately; regenerate the exact bad clip before assembling.

## Pacing correction

When the user says there is too much dead air:

- Shorten the script instead of stretching visuals to match a slow cut.
- Target a punchier 30–40 second reel if that improves tension.
- Use one dramatic beat per clip.
- Remove passive establishing shots.
- Trim/generated voiceover silence before final export.
- Verify with ffmpeg silence detection if available.

## Native vertical correction

For Reels/TikTok/Shorts delivery:

- Source clips should be natively vertical or intentionally reframed to feel native.
- Do not use blurred side-fill or landscape-in-portrait padding as the primary rescue strategy.
- If source clips feel horizontal, regenerate or intentionally crop/reframe around the subject and key action.

## Acceptance checklist

- Same protagonist face, hair, outfit, age, and markers across clips.
- Same scene geography unless the story explicitly moves.
- Hook lands in first 1–2 seconds.
- No passive beat longer than about one second.
- No multi-second narration gaps.
- Final export feels like a native 9:16 short, not adapted landscape footage.
