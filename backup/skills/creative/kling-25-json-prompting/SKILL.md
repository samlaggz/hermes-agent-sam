---
name: kling-25-json-prompting
description: Write timing-aligned JSON prompts for Kling 2.5 text-to-video generation, with script-to-shot sync, camera language, and negative-prompt discipline.
version: 1.0.0
author: <REDACTED_PUBLIC_BACKUP>
license: MIT
created_by: agent
---

# Kling 2.5 JSON Prompting

Use this when generating **Kling 2.5** videos from **text only** and the user wants:
- detailed JSON-style prompts
- scene-by-scene timing that matches narration/script
- strong cinematic motion without separate reference-frame generation
- direct text-to-video prompting in tools like Magnific

## What this skill is based on
Online references reviewed before creating this skill:
- **Official Kling quickstart** (`kling.ai/quickstart/text-to-video-prompt-guide`)
  - Kling prompt formula: **Subject + Subject Movement + Scene + (Camera Language + Lighting + Atmosphere)**
  - Official duration guidance observed there: Kling text-to-video is built around **5s or 10s** clip durations depending on the interface/API
- **Kling API docs** (`klingapi.com/docs`)
  - Request parameters include `prompt`, `duration`, `aspect_ratio`, `mode`, `negative_prompt`
  - Example duration values shown: **5 or 10** seconds
- **Third-party camera movement guide** (`hixx.ai/.../kling-25-prompt`)
  - Useful camera-language vocabulary: slow dolly in, crash zoom, dolly out, dolly zoom, tracking, pedestal up/down, pan, orbit, spiral up

## Core rule: timing sync first
For this user, **script timing and video timing must match before generation**.

Workflow:
1. Write the script as shot-sized narration beats.
2. Measure each beat's target speaking duration.
3. Match each shot to an available Kling duration option.
4. **If Kling does not offer the exact duration you want, rewrite the script beat to fit the available duration** before generating.
5. Generate the clip only after the script beat, prompt beat, and clip duration are aligned.

### Timing policy
- If the interface supports only **5s** and **10s**:
  - rewrite the line to fit 5s or 10s
  - do **not** keep a 7-second narration line and pair it with a 10-second clip unless you explicitly rewrite pacing/VO for the extra time
- Prefer:
  - **5s** for impact beats, reveals, quick shocks, transitions
  - **10s** for escalation, camera travel, atmospheric build, or complex action

## Mandatory prompt structure
Build prompts in this JSON-style shape:

```json
{
  "clip": "clip01",
  "duration_target": "5s or 10s",
  "subject": "who/what is the focus",
  "subject_description": "appearance, wardrobe, age, texture, emotional state",
  "subject_movement": "exact motion suitable for the chosen duration",
  "scene": "location and environmental setup",
  "scene_description": "foreground, background, weather, props, spatial details",
  "camera_language": "shot type + lens feel + framing + camera motion",
  "lighting": "time of day, source, mood, shadow behavior",
  "atmosphere": "emotional tone",
  "style": "cinematic realism / horror realism / etc.",
  "negative_prompt": [
    "no subtitles",
    "no watermark",
    "no logo",
    "no extra limbs",
    "no broken anatomy",
    "no unintended comedy"
  ]
}
```

## How to translate Kling's official formula into JSON
Official formula:
- **Subject**
- **Subject Movement**
- **Scene**
- **Camera Language**
- **Lighting**
- **Atmosphere**

Recommended JSON mapping:
- `subject` + `subject_description`
- `subject_movement`
- `scene` + `scene_description`
- `camera_language`
- `lighting`
- `atmosphere`
- plus `style` and `negative_prompt`

## Writing rules for Kling 2.5

### 1. Keep one clip to one core beat
A single Kling clip should usually contain **one dominant event**:
- one reveal
- one movement progression
- one emotional turn
- one camera idea

Do not cram 3 story beats into one 5s clip.

### 2. Motion must fit the duration
Write movement that can visibly complete inside the selected duration.

Bad for 5s:
- slow corridor walk, door opens, reveal inside room, character screams, camera whips back

Better:
- character freezes as door slowly opens by itself

### 3. Camera language should be explicit
Use concrete camera terms, not vague requests.
Examples:
- slow dolly in
- tracking shot
- low-angle close-up
- handheld push-in
- orbit shot
- slow pan right
- pedestal up
- dolly zoom for panic

### 4. Lighting and atmosphere are not optional
These improve adherence and consistency.
Examples:
- sickly tungsten hallway light
- cold fridge glow
- moonlit blue spill
- oppressive shadows
- damp claustrophobic dread

### 5. Negative prompts should remove common failure modes
For horror/cinematic realism, commonly include:
- no watermark
- no logo
- no subtitles
- no text overlay
- no nested frame effect
- no slapstick or comedy expression
- no distorted face
- no extra fingers
- no duplicate body unless intentionally scripted

## Shot planning method
Before generating, make a timing grid like:

- Clip 1 — 5s — hook reveal
- Clip 2 — 10s — escalating clue
- Clip 3 — 5s — sudden threshold moment
- Clip 4 — 10s — impossible reveal
- Clip 5 — 5s — warning line
- Clip 6 — 5s — final twist sting

Then rewrite the narration so each beat naturally fits the chosen durations.

## Prompt template

```json
{
  "clip": "clipXX",
  "duration_target": "10s",
  "subject": "Mira",
  "subject_description": "late-20s exhausted night-shift nurse, pale, tense, hospital bag slipping from one hand",
  "subject_movement": "she stops mid-step, breathing shallowly, then slowly turns toward the sound as fear rises in her face",
  "scene": "apartment hallway at 3:13 a.m.",
  "scene_description": "narrow corridor, peeling walls, frosted-glass door, chain lock visible, damp floor, weak yellow ceiling light",
  "camera_language": "slow handheld dolly in from behind, medium shot tightening to close-up, shallow depth of field",
  "lighting": "sickly tungsten light with cold blue spill from the stairwell, deep shadow pockets",
  "atmosphere": "claustrophobic supernatural dread",
  "style": "cinematic horror realism",
  "negative_prompt": [
    "no subtitles",
    "no watermark",
    "no logo",
    "no unintended comedy",
    "no broken anatomy",
    "no nested frame effect"
  ]
}
```

## Time-sync checklist before Generate
Before clicking Generate, verify:
- chosen clip duration matches the rewritten narration beat
- prompt action is feasible within that duration
- shot contains only one main dramatic beat
- camera move is feasible within that duration
- aspect ratio is correct
- model is correct
- Unlimited is visible if required by the workflow
- negative prompt removes common failure modes

## Direct text-to-video rule for this user
If the user says **do not generate frames**:
- skip image/reference generation entirely
- generate clips directly from prompt text
- compensate by making the prompt more explicit about:
  - subject identity
  - movement progression
  - camera motion
  - environment details
  - lighting
  - emotional tone

## Pitfalls

### Mismatch between narration and clip duration
If the narration line takes 7 seconds and the interface only gives 5 or 10, rewrite the line first.

### Overstuffed prompt action
One clip should not contain a whole paragraph of events.

### Vague camera requests
"cinematic" alone is weak. Use explicit shot vocabulary.

### Prompting beyond visible time
Do not describe a long chain of sequential actions that cannot plausibly happen in the selected duration.

## Recommended output format for planning
When building a project, first produce:
1. shot list with durations
2. rewritten narration lines matched to those durations
3. JSON prompts matched to each clip
4. only then begin generation
