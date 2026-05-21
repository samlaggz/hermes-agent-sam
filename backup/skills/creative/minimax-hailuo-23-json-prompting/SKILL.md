---
name: minimax-hailuo-23-json-prompting
description: Write detailed JSON-style prompts for MiniMax Hailuo 2.3 text-to-video generation with 6s/10s timing sync, bracket camera commands, and narration-to-shot alignment.
version: 1.0.0
author: <REDACTED_PUBLIC_BACKUP>
license: MIT
created_by: agent
---

# MiniMax Hailuo 2.3 JSON Prompting

Use this when generating videos with **MiniMax Hailuo 2.3** and the user wants:
- direct text-to-video when supported by the UI
- detailed JSON-style prompting
- tight sync between narration timing and clip timing
- stronger motion, composition, facial expression, and cinematic control than a rough draft model

## Basis for this skill
This skill is based on online references already reviewed in-session:

1. **Official MiniMax API docs**
   - `MiniMax-Hailuo-2.3` is a supported text-to-video model
   - text-to-video prompt field supports camera control with bracket syntax
   - observed supported duration values for Hailuo 2.3: **6 or 10 seconds**
   - observed supported camera commands include:
     - `[Truck left]`, `[Truck right]`
     - `[Pan left]`, `[Pan right]`
     - `[Push in]`, `[Pull out]`
     - `[Pedestal up]`, `[Pedestal down]`
     - `[Tilt up]`, `[Tilt down]`
     - `[Zoom in]`, `[Zoom out]`
     - `[Shake]`
     - `[Tracking shot]`
     - `[Static shot]`
   - combined camera commands can appear inside one bracket
   - sequential moves can be written in prompt order
   - `prompt_optimizer` and `fast_pretreatment` exist in the API layer

2. **Magnific MiniMax Hailuo 2.3 guide**
   - Hailuo 2.3 supports text and image inputs
   - stronger output quality than the Fast version
   - suited for final content, expressive motion, richer detail, stylized scenes, facial micro-expression, and cinematic motion
   - prompt guidance emphasizes explicit subject, action, style, motion, lighting, and camera wording

## Timing rule
For this user, **narration timing must match clip timing before generation**.

### Duration policy
Plan around **6s** and **10s** clips.

Workflow:
1. Write narration as shot-sized beats.
2. Choose whether each beat is a 6s or 10s clip.
3. If the line does not fit 6 or 10 seconds naturally, rewrite the line before generation.
4. Keep the action in the prompt feasible within that chosen duration.

### Suggested usage
- **6s** for:
  - hooks
  - reveals
  - stings
  - quick emotional turns
- **10s** for:
  - buildup
  - richer camera travel
  - layered performance beats
  - more complex spatial transitions

## Prompt planning format
Use JSON-style planning even if the Magnific UI takes plain text.

```json
{
  "clip": "clip01",
  "duration_target": "6s",
  "subject": "Mira",
  "subject_description": "late-20s exhausted night-shift nurse, tense eyes, hospital bag in hand, pale face",
  "action": "she freezes when three knocks come from inside her locked apartment door",
  "scene": "narrow apartment hallway at 3:13 a.m.",
  "scene_description": "frosted-glass door, chain lock still on, damp floor, peeling walls, cramped corridor",
  "camera_motion": "[Push in]",
  "camera_language": "medium shot tightening toward close-up, shallow depth of field",
  "lighting": "sickly tungsten hall light mixed with cold blue stairwell spill",
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

## Converting the JSON plan into the actual Hailuo prompt
Write the final prompt as detailed prose with bracket camera commands embedded.

Example:

```text
Mira, a late-20s exhausted night-shift nurse with pale tense features and a hospital bag in one hand, freezes in a narrow apartment hallway at 3:13 a.m. when three knocks come from inside her locked frosted-glass apartment door. The chain lock is still on, the walls are peeling, and the damp corridor feels cramped and oppressive. [Push in] Medium shot tightening toward close-up with shallow depth of field. Sickly tungsten hallway light mixes with cold blue stairwell spill. Claustrophobic supernatural dread. Cinematic horror realism. No subtitles, no watermark, no logo, no comedy, no broken anatomy, no extra limbs, no distorted face.
```

## Mandatory components
Every MiniMax Hailuo 2.3 prompt should cover:
1. subject
2. subject description
3. action / motion progression
4. scene / environment
5. camera movement with bracket commands when useful
6. shot language
7. lighting
8. atmosphere
9. style
10. negative constraints

## Camera command rules
Use official-style square bracket motion commands.

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

### Combined movement
Use up to about 2–3 simultaneous directions when necessary.

Good:
- `[Pan left,Pedestal up]`

### Sequential movement
Write them in narrative order.

Example:
- `The duplicate slowly raises her head. [Push in], then Mira recoils and the room seems to widen around her. [Pull out]`

## Writing rules for Hailuo 2.3

### 1. One clip = one dominant dramatic beat
Do not overload a clip with too many events.

### 2. Motion must fit the duration
If the clip is 6 seconds, describe motion that can visibly complete inside 6 seconds.

### 3. Use explicit movement verbs
Examples:
- freezes
- recoils
- slowly turns toward camera
- raises head unnaturally slowly
- hand slams against glass
- takes one step back
- breath catches

### 4. Use expression detail
Hailuo 2.3 is strong at facial micro-expression and emotional nuance. Include specific face/body signals:
- jaw tightens
- eyes widen
- lips tremble
- expression shifts from confusion to panic

### 5. Use strong environment cues
Examples:
- wet tile reflections
- rotting baseboards
- weak fridge glow
- black mold in the corners
- warped wallpaper
- stale fogged glass

### 6. Use style + lighting deliberately
Examples:
- cinematic supernatural horror realism
- cold corpse-blue side light
- oppressive yellow tungsten hallway lighting
- dead reflections and damp shadow pockets

## Timing sync checklist before Generate
Before clicking Generate, verify:
- narration line fits 6s or 10s naturally
- chosen duration matches rewritten line
- model is **MiniMax Hailuo 2.3**
- prompt contains one main beat
- camera movement is explicit but not overloaded
- subject/action/scene/lighting/style are all present
- negative constraints are present
- aspect ratio is correct
- Unlimited is visible if required
- no stale reference is attached if running text-to-video
- protagonist identity markers are repeated consistently across clips (same hair, wardrobe, face shape, role cues)
- environment anchors are repeated consistently across clips (same door, hallway, kitchen, threshold, palette)
- the output is likely to read as native 9:16 composition, not landscape footage later stuffed into a portrait wrapper

## Standard-vs-Fast rule
For this user:
- **MiniMax Hailuo 2.3 Fast** = fast drafts / quick testing
- **MiniMax Hailuo 2.3** = better fit when the user explicitly wants the stronger version instead of Fast

So when the user switches from Fast to Standard, treat the Standard model as the preferred generation path for the actual production attempt.

## Good horror example

```json
{
  "clip": "clip05",
  "duration_target": "6s",
  "subject": "duplicate Mira",
  "subject_description": "corpse-pale duplicate of Mira, wet hair hanging over her face, hollow eyes, hospital badge hanging crooked",
  "action": "she leans in slightly and whispers a warning, then lifts one shaking finger to point behind Mira",
  "scene": "rotting duplicate apartment interior",
  "scene_description": "water-stained walls, dark flooded floor edges, warped ceiling, dead silence",
  "camera_motion": "[Push in]",
  "camera_language": "tight close-up with subtle creeping approach",
  "lighting": "cold corpse-blue side light with darkness swallowing the frame edges",
  "atmosphere": "intimate terror and impossible truth",
  "style": "cinematic paranormal horror realism",
  "negative_prompt": [
    "no subtitles",
    "no watermark",
    "no logo",
    "no comedy",
    "no broken anatomy",
    "no extra fingers",
    "no unintended duplicate bodies"
  ]
}
```

## Pitfalls

### Wrong duration for the narration line
If the line reads like 8 seconds, rewrite it to 6 or 10 before generating.

### Weak motion wording
Hailuo performs better with concrete movement language.

### Overloaded camera commands
Too many simultaneous directions reduce clarity.

### Treating Standard like a vague one-shot magic box
Even with the stronger model, prompt discipline still matters.

## Recommended workflow output
Before generation, produce:
1. shot list with 6s/10s durations
2. rewritten narration lines matched to those durations
3. JSON prompts for each clip
4. then generate in sequence

## Native-reel and pacing validation

For this user, a successful Hailuo 2.3 result is not just "technically vertical" — it must feel like a native Reel/Short.

Add these checks:
- After downloading the generated clips, verify their actual frame dimensions before assembly.
- If the model/settings path produced landscape clips that require blurred side-fill inside a portrait export, reject that assembly path and regenerate or reframe intentionally.
- Prefer shorter, punchier narration over stretching a weak beat to fill the full duration budget.
- If the voice track contains multi-second silence between beats, trim/regenerate it before calling the cut finished.
