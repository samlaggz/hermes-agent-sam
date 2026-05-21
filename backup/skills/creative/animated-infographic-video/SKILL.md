---
name: animated-infographic-video
description: Build short illustrated explainer videos with moving infographics, map scenes, voiceover, and phone-safe exports.
version: 0.1.0
author: <REDACTED_PUBLIC_BACKUP>
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [video, infographic, animation, maps, ffmpeg, tts, motion-graphics]
---

# Animated Infographic Video

Use this when the user wants an **infographic video**, **illustrated explainer**, **moving map breakdown**, **YouTube-style explainer**, or rejects a static infographic with feedback like "not like this", "I want motion", "make it like this video", or "show it on a map".

This skill exists for the class of work where a static infographic is not enough. The output is a short, visual story with animated scenes, labels, icons, transitions, and optional narration.

## Trigger Conditions

Load this skill when any of these are true:
- The user wants a **video**, not a still image.
- The user references a YouTube explainer, motion-graphics reel, or animated infographic as the target style.
- The user asks for **moving illustrations**, **map-based conflict/economics/geopolitics explainers**, or scene-by-scene visual storytelling.
- A first pass as slides/cards/static infographic was rejected for being too static.

## Core Principle

**Do not respond to a motion-graphics brief with static slides unless the user explicitly asked for slides.**

If the user says they want something "like this video," extract the **visual grammar** of the reference:
- pacing
- scene count
- map usage
- camera movement
- icon style
- information density
- typography hierarchy
- voiceover cadence

Then reproduce that grammar with original assets/workflows.

## Default Output Targets

Unless the user says otherwise:
- Length: **35–60 seconds**
- Aspect: **16:9 landscape**
- Safe area: keep important text within a central mobile-safe region
- Export: **H.264 + yuv420p + AAC + faststart**
- Motion: readable on phones first, desktop second

## Recommended Workflow

### 1) Lock the brief
Extract and restate:
- audience
- runtime target
- reference style
- visual mode: map / timeline / comparison / mechanism / forecast
- whether narration, captions, music, or silent delivery is desired

If the user already corrected a prior attempt, treat that correction as binding design input.

### 2) Ground the facts before animating
For current events, conflicts, markets, policy, or geography:
- verify locations, names, and directional claims from current reporting
- distinguish **confirmed facts** from **pressure/risk/scenario language**
- avoid overclaiming contested battlefield or political outcomes

For conflict maps especially:
- show clearly labeled places
- use cautious wording when closure/blockade/control is uncertain
- prefer "pressure", "disruption risk", "reported strike site", "shipping corridor", etc. where appropriate

### 3) Build a visual script, not just a text script
Plan 4–7 scenes max for a ~50 second explainer.
For each scene define:
- scene goal
- on-screen text
- animated elements
- map/camera movement
- icon overlays
- narration lines
- transition in/out

### 4) Choose the rendering path
Pick the simplest path that matches the brief:

**A. Local custom renderer**
Use Python/PIL or SVG/HTML frame rendering + FFmpeg when you need:
- exact layouts
- map overlays
- deterministic icon placement
- no extra API dependency
- fast iteration on labels/colors/positions

**B. Manim / procedural animation**
Use when the scene is mathematical, diagrammatic, or benefits from vector animation primitives.

**C. Image/video generation stack**
Use when the user wants a more painterly / cinematic / generative look and accepts the variability.

Default to **local deterministic rendering** when the user asks for clean infographic clarity.

### 5) Design rules for illustrated map explainers
- Start with a simple regional base map; avoid clutter.
- Use 1 visual idea per scene.
- Animate lines/arrows/routes before dumping labels.
- Use boxed callouts for narrow waterways, corridors, chokepoints, or contested zones.
- Keep labels short: place name + 1 role.
- Use icons for missiles/drones/ships/air/insurance/oil instead of sentence-heavy panels.
- If a panel grows beyond 3 bullets, split the scene.
- Prefer bold typography hierarchy over dense prose.

## User Preference Lessons Embedded

When a user rejects a first pass as "not like this" and asks for **interactive illustrated moving infographics**:
- pivot away from slide decks/cards immediately
- add **camera motion**, **route lines**, **map callouts**, and **scene-based storytelling**
- keep the pacing concise and visual
- make the first revision materially different, not a cosmetic refresh of the static version

When the user says the graphics feel unattractive, too map-only, or too rough:
- switch from placeholder/custom shapes to **real sourced vector assets** as early as possible
- if Magnific is already logged in, prefer its authenticated **illustrations / vectors** library because it may work even when direct public Freepik-family pages are blocked
- for conflict/documentary explainers, broaden beyond maps to a **character-led visual mix**: soldiers, fighter jets, missiles, drones, skyline silhouettes, chokepoint maps, and icon systems
- use maps as the geographic backbone, not the entire visual language

When the user asks for something that "hooks the watcher in the first 3 seconds":
- open with a **cold-open hero frame** before the explanatory map build
- use one strong headline, one short subhead, and 2–3 supporting badges max
- lead with dramatic silhouettes / aircraft / alert shapes first, then transition into the map logic
- do not spend the opening beats on slow information setup

When the user says the animation is "going here and there" or feels unfocused:
- reduce decorative movement and keep motion strictly tied to narrative purpose
- each scene should have one dominant animated idea only: fly-in, pulse, route reveal, marker pop, ship movement, or skyline rise
- avoid multiple competing motions in the same frame unless one is clearly background texture
- prefer short, assertive scene timing over constant ambient drift

When the user asks for the **most attractive documentary style** rather than a map-only explainer:
- switch to a **hook-first cold open** built around one dramatic headline plus 1-2 hero visual elements (for example soldiers, fighter jets, missiles, skyline, alert rings)
- do not spend the first 3 seconds teaching geography; spend them creating tension, then transition into explanation
- use a **character-led war-documentary mix**: maps for orientation, but soldiers / aircraft / weapons / skyline silhouettes for emotional pull
- keep the runtime tighter and more forceful than a slow explainer when the user explicitly asks for stronger engagement
- prefer a dark cinematic grade and strong contrast over soft infographic flatness for this style class

When the user says the graphics or illustrations look **bad / rough / homemade**, treat that as a hard signal to change the asset pipeline, not just the layout:
- stop relying on placeholder custom drawings for the next pass
- source **real vector assets, map art, icons, and stock illustration packs** before rendering again
- if Magnific is already authenticated, check **Magnific stock / illustrations / vectors** first because it may expose usable Freepik-family assets even when direct browser access to Freepik is blocked
- prefer **map-heavy newsroom / documentary graphics** over character-heavy editorial scenes for war, geopolitics, logistics, or Gulf-market explainers unless the user explicitly asks for character illustration
- verify at least one actual downloadable asset from the authenticated library before promising a premium rebuild

## Audio Guidance

- Narration should match scene timing, not the reverse.
- Draft voiceover early, then trim or pad to target runtime.
- Keep delivery concise and concrete.
- Background music should support, not compete with, callouts.

## Export Checklist

Always verify final output for phone compatibility:
- container: mp4
- video codec: H.264
- pixel format: yuv420p
- audio codec: AAC
- faststart enabled
- no unusual 4:4:4 profile unless explicitly requested

## Deliverables

Minimum deliverables:
- final video file
- short note on runtime / codec / dimensions
- source or script notes if the project is likely to be iterated

## References

- `references/rendering-checklist.md` — concise production checklist for short animated infographic explainers
- `references/art-direction-and-asset-sourcing.md` — reference-matched sourcing order, Magnific-first asset checks, and lessons from replacing rough custom illustrations with real vector/map assets
- `references/war-documentary-map-infographics.md` — map-first documentary structure for conflict explainers, including choke-point scenes, weapons-category framing, and UAE/Gulf consequence panels
- `references/hook-first-character-led-documentaries.md` — session-tested guidance for rebuilding weak map-only war explainers into faster, more attractive hook-first documentary videos with soldier / jet / skyline / chokepoint asset mixes and tighter motion rules
- `references/premium-war-documentary-assets.md` — Magnific search queries, asset classes, and composition lessons for more attractive hook-first war-documentary videos
- `references/youtube-documentary-channel-patterns.md` — repeatable YouTube channel angles, niche recommendations, and hook structures for documentary/explainer content Hermes can produce strongly

## Pitfalls

1. **Static-slide trap** — a user asking for a reference-video style usually wants motion language, not prettier slides.
2. **Overcrowded maps** — if labels collide, split scenes instead of shrinking everything.
3. **Unverifiable claims** — for live conflicts, avoid visually presenting speculation as settled fact.
4. **Desktop-only composition** — large edge text and tiny captions often fail on phones.
5. **Bad mobile encoding** — H.264 4:4:4 or unusual audio/container choices cause playback failures on phones.
6. **Narration drift** — if scenes do not line up with the voiceover, shorten the script before adding more graphics.
