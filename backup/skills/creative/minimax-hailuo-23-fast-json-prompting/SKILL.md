---
name: minimax-hailuo-23-fast-json-prompting
description: Write detailed JSON-style prompts for MiniMax Hailuo 2.3 Fast text-to-video generation with timing sync, motion-first prompting, and draft-to-final iteration rules.
version: 1.0.0
author: <REDACTED_PUBLIC_BACKUP>
license: MIT
created_by: agent
---

# MiniMax Hailuo 2.3 Fast JSON Prompting

Use this when generating videos with **MiniMax Hailuo 2.3 Fast**, especially in Magnific, and the user wants:
- direct text-to-video generation
- detailed JSON-style prompts
- narration and shot timing to match closely
- strong motion, facial expression, and cinematic prompt control
- a fast iteration model before committing to final renders

## What this skill is based on
Online references reviewed before creating this skill:

1. **Official MiniMax API docs** (`platform.minimax.io/docs/api-reference/video-generation-t2v`)
   - `model` supports `MiniMax-Hailuo-2.3`
   - `prompt` is the main text description field
   - supported `duration` values shown for Hailuo 2.3: **6 or 10 seconds**
   - supported camera control syntax for Hailuo-family text-to-video uses **bracket commands** such as:
     - `[Truck left]`, `[Truck right]`
     - `[Pan left]`, `[Pan right]`
     - `[Push in]`, `[Pull out]`
     - `[Pedestal up]`, `[Pedestal down]`
     - `[Tilt up]`, `[Tilt down]`
     - `[Zoom in]`, `[Zoom out]`
     - `[Shake]`
     - `[Tracking shot]`
     - `[Static shot]`
   - multiple commands can be combined inside one bracket: `[Pan left,Pedestal up]`
   - sequential moves can be written in order: `...[Push in], then ...[Pull out]`
   - `prompt_optimizer` exists; disable it when you need stricter manual control
   - `fast_pretreatment` exists for MiniMax-Hailuo-2.3 and MiniMax-Hailuo-02 when optimizer is enabled

2. **Magnific guide for MiniMax Hailuo 2.3** (`magnific.com/blog/minimax-hailuo-2-3`)
   - Hailuo 2.3 supports **text and image inputs**
   - Hailuo 2.3 Fast is intended for **quick previews, idea testing, and fast iterations**
   - prompt guidance emphasizes:
     - clear motion keywords
     - explicit subject + action + style
     - camera movement language
     - lighting and atmosphere cues
   - strong use cases include expressive character scenes, stylized visuals, social content, and rapid iteration

## Core timing rule
For this user, **script timing and clip timing must align before generation**.

### Duration policy
For Hailuo 2.3 / Hailuo 2.3 Fast, plan around **6s** and **10s** clips.

Workflow:
1. Write the narration in shot-sized beats.
2. Decide whether each beat is best as **6s** or **10s**.
3. If the beat does not fit 6 or 10 seconds, **rewrite the narration beat before generating**.
4. Keep the prompt action feasible within the selected duration.

### Practical guidance
- Use **6s** for:
  - reveals
  - jump moments
  - single emotional turns
  - short punchy hooks
- Use **10s** for:
  - camera travel
  - buildup beats
  - multi-part motion within a single scene
  - more atmospheric dread or escalation

## Prompt design philosophy
Hailuo 2.3 Fast is best when prompts are:
- explicit
- motion-aware
- visually concrete
- limited to one strong dramatic beat per clip

Do not write vague prompts like:
- "make it cinematic horror"

Instead, specify:
- subject
- action progression
- environment
- lighting
- style
- camera movement using bracket commands
- mood
- what to avoid

## Recommended JSON-style prompt shape
Use this structure when planning prompts, even if the UI only accepts plain text. The JSON acts as the planning representation.

```json
{
  "clip": "clip01",
  "duration_target": "6s",
  "subject": "Mira",
  "subject_description": "late-20s exhausted night-shift nurse, pale skin, tense expression, hospital bag in one hand",
  "action": "she freezes as three knocks come from inside her locked apartment door and her breathing turns shallow",
  "scene": "narrow apartment corridor at 3:13 a.m.",
  "scene_description": "peeling walls, frosted-glass door, chain lock visible, damp floor, cramped hallway",
  "camera_motion": "[Push in]",
  "camera_language": "medium shot tightening toward close-up, shallow depth of field, oppressive framing",
  "lighting": "sickly tungsten ceiling light with cold blue spill from the stairwell",
  "atmosphere": "claustrophobic supernatural dread",
  "style": "cinematic horror realism",
  "negative_prompt": [
    "no subtitles",
    "no watermark",
    "no logo",
    "no comedy",
    "no broken anatomy",
    "no extra limbs",
    "no distorted face"
  ]
}
```

## How to convert JSON plan into a Hailuo prompt
The actual text prompt should usually read like polished cinematic prose with embedded camera commands.

Example conversion:

```text
Mira, a late-20s exhausted night-shift nurse with a pale tense face and a hospital bag in one hand, freezes in a narrow apartment corridor at 3:13 a.m. as three knocks come from inside her locked frosted-glass apartment door. The chain lock is still visible, the peeling hallway walls are damp, and the space feels cramped and oppressive. [Push in] Medium shot tightening toward close-up with shallow depth of field. Sickly tungsten ceiling light mixes with cold blue stairwell spill. Claustrophobic supernatural dread. Cinematic horror realism. No subtitles, no watermark, no logo, no comedy, no broken anatomy, no extra limbs, no distorted face.
```

## Mandatory components
Every Hailuo 2.3 Fast prompt should explicitly cover:
1. **Subject**
2. **Action**
3. **Scene/environment**
4. **Camera movement** using bracket syntax when useful
5. **Shot language**
6. **Lighting**
7. **Atmosphere/mood**
8. **Style**
9. **Negative constraints**

## Camera command rules
Officially observed syntax uses square brackets.

### Supported examples
- `[Truck left]`
- `[Truck right]`
- `[Pan left]`
- `[Pan right]`
- `[Push in]`
- `[Pull out]`
- `[Pedestal up]`
- `[Pedestal down]`
- `[Tilt up]`
- `[Tilt down]`
- `[Zoom in]`
- `[Zoom out]`
- `[Shake]`
- `[Tracking shot]`
- `[Static shot]`

### Combining moves
Use no more than about 2–3 movements at once.

Good:
- `[Pan left,Pedestal up]`

Too busy:
- 5 different camera moves in one moment

### Sequential moves
Write them in narrative order.

Example:
- `The figure slowly turns toward camera. [Push in], then the door behind her swings open. [Pull out]`

## Shot-writing rules

### 1. One clip = one dominant beat
Do not force several story events into one clip.

### 2. Keep action duration-realistic
If the clip is 6 seconds, do not describe a long dramatic chain that needs 12 seconds.

### 3. Motion keywords matter
Magnific's own Hailuo guide emphasizes explicit motion phrasing. Use verbs like:
- turns toward viewer
- glides forward
- recoils
- steps back slowly
- raises head unnaturally slowly
- hand slams against glass

### 4. Expression detail is valuable
Hailuo is good at micro-expression and character emotion, so specify emotion changes:
- eyes widen
- lips tremble
- jaw tightens
- expression shifts from confusion to panic

### 5. Style cues should be specific
Examples:
- cinematic horror realism
- high-contrast cinematic night lighting
- damp haunted-apartment realism
- stylized supernatural realism

## Timing sync checklist before Generate
Before clicking Generate, verify:
- narration line fits 6s or 10s naturally
- selected clip duration matches rewritten line
- prompt contains a single dominant beat
- camera movement is explicit and not overloaded
- subject/action/scene/lighting are all present
- negative constraints are present
- model is **MiniMax Hailuo 2.3 Fast**
- aspect ratio is correct
- Unlimited is visible if required by the workflow

## Fast-model workflow guidance
Because Hailuo 2.3 Fast is best for rapid iteration:
1. Plan tightly.
2. Generate a disciplined first pass.
3. If a clip is bad, fix it **immediately at that clip**.
4. Do not postpone obvious repair until the end.
5. Once the sequence works, assemble and then add VO/music.

## Good horror prompt example

```json
{
  "clip": "clip04",
  "duration_target": "10s",
  "subject": "duplicate Mira",
  "subject_description": "corpse-pale version of Mira in hospital scrubs, wet hair, hollow exhausted eyes",
  "action": "she stands motionless at the far end of a rotting duplicate apartment, then slowly lifts her head and fixes Mira with a dead stare",
  "scene": "decayed copy of the apartment interior",
  "scene_description": "water-damaged walls, flooded baseboards, black stains, dead air, warped floor, hallway receding behind her",
  "camera_motion": "[Push in]",
  "camera_language": "wide doorway reveal moving into a slow creeping approach",
  "lighting": "cold grey rot-light with weak spill from the original hallway",
  "atmosphere": "surreal reality rupture and existential dread",
  "style": "cinematic supernatural horror realism",
  "negative_prompt": [
    "no subtitles",
    "no watermark",
    "no logo",
    "no slapstick expression",
    "no broken anatomy",
    "no extra fingers",
    "no accidental duplicate bodies beyond the intentional double"
  ]
}
```

## Pitfalls

### Mismatch between narration and duration
If a line reads like 8 seconds, rewrite it to 6 or 10 before generation.

### Weak motion language
Hailuo responds better when movement is described concretely.

### Too many camera directions
Too many motion commands can muddy the result.

### Treating Fast like a final-polish model
Use it for fast, smart iteration — but still keep prompts disciplined enough that outputs can be assembly-worthy.

## Recommended workflow output
Before generation, produce:
1. shot list with chosen 6s/10s durations
2. rewritten narration lines fitted to those durations
3. JSON prompts for each clip
4. then generate in sequence
