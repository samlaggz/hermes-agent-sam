---
name: magnific-short-video-production
description: Produce short-form videos with Magnific using the live browser workflow, model selection strategy, detailed JSON prompting, and external voiceover assembly.
version: 1.0.0
author: <REDACTED_PUBLIC_BACKUP>
license: MIT
created_by: agent
---

# Magnific Short Video Production

Use this when the user wants short-form video made through **Magnific's Video Generator** — especially anime-inspired shorts, cinematic shorts, or social clips that need **model selection inside Magnific**, **detailed prompting**, and **voiceover assembled outside Magnific**.

## Trigger conditions

Load this skill when any of these are true:
- The user asks to make a video in **Magnific** rather than with a local image/video pipeline.
- The user wants you to inspect **Models → All models** and choose the best option.
- The user wants **anime-inspired**, **cinematic**, or **viral short** output.
- The user wants a **45–90 second short**, but Magnific's best available model only produces short clips that must be stitched together.
- The user wants **Andrew voice** or another external TTS voice over a Magnific-generated video.
- The user uploads a real-estate brochure/PDF and asks for a branded luxury teaser using stock/generated footage, especially when the output must be landscape, watermark-free, location-correct, and based on brochure amenities/location/brand facts.

## Core workflow

1. **Check Magnific access first**
   - Open the existing live/CDP-backed browser session if available.
   - Verify login state before generating or downloading anything.
   - If the user has explicitly said to always check login first, do that before touching generation controls.

2. **Open Video Generator, not Image Generator**
   - Go to `Video Generator`.
   - If starting from an existing image result, prefer `Create video` from that image so the `Start image` reference is populated automatically.

3. **Inspect model options in `All models`**
   - Do not assume `Auto` is best when the user explicitly wants model selection.
   - Open the model picker and inspect `All models`.
   - Choose based on three axes:
     - supports the requested visual style,
     - available under the user's plan,
     - realistic duration/resolution tradeoffs.

4. **For anime / illustration-friendly unlimited generation**
   - Prefer **Kling 2.5** when the goal is anime-inspired or illustration-and-animation output and the user wants **Unlimited** generation.
   - Reason: it supports `Illustration & animation` and can run in Unlimited mode.
   - After choosing it, check whether the current resolution is compatible; if not, use the UI link/button to **Switch to Unlimited mode**.

5. **Know the limitation: long shorts are multi-clip jobs**
   - Magnific's strongest unlimited anime-capable option is still a **short-clip generator**, not a one-shot 45–90 second generator.
   - Therefore, a proper 45–90 second short should be planned as:
     - 5–10 short clips,
     - each with one strong story beat,
     - stitched later in editing,
     - synced to narration externally.

6. **Use detailed JSON-style prompting**
   - When the user asks for detailed prompting, structure the prompt like JSON with keys such as:
     - `scene`
     - `character`
     - `setting`
     - `action`
     - `camera`
     - `mood`
     - `lighting`
     - `style`
     - `motion`
     - `negative`
   - This improves controllability and makes future clip prompts easier to vary systematically.

7. **For viral shorts, script before generating**
   - Write the story beats before generating clips.
   - For Shorts/TikTok/Reels pacing:
     - hook inside first 1–3 seconds,
     - no dead establishing opening,
     - every shot must carry story,
     - end with a cliffhanger or forcing question.
   - For 45–90 second crime-thriller anime shorts, use a structure like:
     - hook reveal,
     - impossible clue,
     - chase/escalation,
     - twist identity reveal,
     - final cliffhanger.

8. **Attach reference image when possible**
   - If a compelling starter image already exists, use `Create video` from that image/result card.
   - Verify the left panel shows `Start image` populated before generating.
   - This materially improves consistency for anime protagonist shots.
   - **But inspect the reference itself before reusing it.** Do not blindly pick the most recent image/video result as the start image.
   - Reject any candidate reference that already contains a visible screen, video frame, picture-in-picture look, embedded border, or nested composition artifact. Those defects propagate into later video clips.
   - For anime shorts, prefer a **clean portrait/reference frame** of the protagonist with no UI-like framing artifacts, then reuse that same clean reference for downstream clips.

9. **Queue clips opportunistically, but recover from capacity modals**
   - If Kling 2.5 Unlimited is available, queue sequential clips as soon as the form is valid.
   - If Magnific shows a modal like `Kling 2.5 is temporarily at full capacity`, first close it and retry briefly.
   - If the model remains saturated, immediately open `Model -> All models` and switch to **another Unlimited-capable model** instead of stalling the whole workflow.
   - Before switching, verify the replacement model still supports the target format/style well enough for the current shot.
   - Preserve the shot plan and continue from the next required clip; do not discard already queued clean-reference clips.

10. **Capacity / limit handling discipline**
   - Keep working through temporary limit or capacity messages instead of treating them as stopping points.
   - Read the wait time Magnific gives, when present.
   - Sleep that amount and retry automatically.
   - Do not end the task just because one retry hit a limit modal.
   - Track whether any **new video generation** has successfully started during the current blocked stretch.
   - Only stop and report the blockage if **more than 45 continuous minutes** pass without being able to successfully start any new generation.
   - Otherwise continue until the requested video work is finished.

11. **Verify every setting before every generate click**
   - Before pressing `Generate`, explicitly verify:
     - correct model selected,
     - Unlimited mode enabled when intended,
     - correct aspect ratio,
     - correct duration,
     - clean `Start image` / reference present,
     - prompt matches the intended clip ID/beat,
     - no stale framed/nested-screen reference is still attached.
   - Treat this as a checklist, not a casual glance.

11. **Generate in sequence: frames first, then videos**
   - For continuity-heavy shorts, first generate or select the clean image/reference frames you intend to use.
   - Only after the reference set is validated should you move into video generation for the sequential clips.
   - This avoids wandering the UI and prevents mixing bad references into later clips.

12. **Voiceover is external**
   - Generate Magnific visuals first.
   - Produce narration separately with TTS.
   - For the user's preferred Andrew voice, use `en-US-AndrewNeural` and assemble the final audio externally.

10. **Assemble outside Magnific**
   - Download the generated clips.
   - Stitch them into one vertical short.
   - Sync Andrew narration and optional music/effects.
   - Export a mobile-friendly MP4.

## Andrew voice workflow

For longer scripts, generate Andrew voice in chunks rather than one long request.

Recommended pattern:
- voice: `en-US-AndrewNeural`
- slightly slower delivery for thriller narration: around `-5%` to `-8%`
- chunk by sentence groups under roughly 250–260 chars
- concatenate the MP3 chunks with ffmpeg

This avoids long-request instability and produces a clean final narration track.

## User-specific workflow preference: true-video shorts only
When the user asks for a short/reel/TikTok-style deliverable from Magnific and criticizes a result for being "images" or "still-image motion," switch immediately to a **plan-first, clip-first** workflow:

1. Write the full cut list before generating anything.
2. Specify per-cut duration, aspect ratio, story beat, and prompt.
3. Generate **every scene as a true video clip** in Magnific; do not rely on Ken Burns, zoom-pan, or image-to-video hybrids for the main body.
4. Keep the first 1-3 seconds reserved for a strong hook.
5. Only after all clips exist, assemble VO/music/captions in post.
6. If a prototype violates this, discard it and restart cleanly rather than iterating on the flawed hybrid.

For this user, a "proper video" means the deliverable is built primarily from native generated clips, stitched into a final vertical short.

### Native reel framing and continuity override
When the user rejects a Magnific short for **character inconsistency**, **scene inconsistency**, **dead audio space**, or **not feeling like a real Reel**, treat that as a workflow correction, not a cosmetic note.

Apply all of the following on the redo:
1. **Continuity beats text-only purity.** If direct text-to-video causes character drift or environment drift, switch to a consistency-first workflow using a clean reusable start/reference image for the protagonist and environment.
2. **Reject fake vertical delivery.** Do not deliver landscape clips inside a blurred-background portrait wrapper. If the generated assets are not compositionally usable as a native-looking 9:16 short, regenerate or reframe intelligently from source footage without the boxblur-sidefill cheat.
3. **Lock a character bible.** Keep the same face shape, hair, outfit, palette, and role markers across every prompt for the protagonist.
4. **Lock environment geography.** Keep the same front door, hallway, kitchen, threshold, and lighting palette across clips unless the story explicitly changes location.
5. **Tighten narration aggressively.** Remove multi-second silent gaps, shorten lines when necessary, and prefer a punchier 30–40 second cut over a slower 45–60 second cut when that improves social-video pacing.
6. **Every shot must advance tension.** Remove dead visual beats and long establishing pauses; the hook should land in the first 1–2 seconds.

See also `references/true-video-shorts-workflow.md` for a concise plan-first clip-generation workflow and anti-pattern checklist.

## Operational notes discovered in live Magnific use

- User-preferred production sequence for Magnific shorts:
  1. Discard stale project outputs before starting a new concept.
  2. Write the full short script and cut plan first.
  3. Generate all required clean reference images before relying on video generation.
  4. While one video is generating or blocked on queue/capacity, prepare the next frame image to keep throughput high.
  5. For each clip, use a clean start image first, then generate video from that image.
- Reuse-first rule for already-generated frames/results:
  - If usable reference frames already exist in the project, do **not** regenerate them in bulk just for naming consistency or a "fresh rebuild".
  - Audit what already exists, keep the best frame per clip, and regenerate only the exact weak or missing frame.
  - If the user says "use the ones you created so far," treat that as a hard constraint and continue directly into video generation.
- First-time quality rule:
  - Make each frame acceptable at the moment it is generated.
  - If a frame looks wrong, retry or fix it **immediately right there**, not at the end of the workflow after several downstream generations have already depended on it.
- For video model selection in this workflow, restrict fallback choices to:
  - Kling 2.5
  - MiniMax Hailuo 2.3 Fast
- For video model selection in this workflow, restrict fallback choices to:
  - Kling 2.5
  - MiniMax Hailuo 2.3 Fast
  - MiniMax Hailuo 2.3
- If a model is busy and Magnific gives a wait estimate, wait that exact amount of time, retry automatically, and keep looping. Do not stop the task on the first limit message.
- Use a **reuse-first** policy for reference frames: if good clip frames already exist in the Magnific creations grid, reuse them instead of regenerating a fresh batch for naming/consistency reasons alone.
- If a frame looks wrong, weak, or inconsistent, retry **immediately at that clip** before moving on. Do not postpone cleanup to the end of the project.
- Before every image or video Generate click, verify the button itself shows `Generate` with the `Unlimited` indicator visible on the control when the selected model/mode supports Unlimited; do not rely only on surrounding labels. For MiniMax Hailuo 2.3 Standard, the button may show plain `Generate` while the left panel still verifies model, reference, duration, and 9:16.
- In Magnific's contenteditable prompt field, `browser_type` may append instead of replacing text. If the old prompt remains, replace via browser console/CDP by setting the contenteditable element's `innerText` and dispatching `InputEvent('input')` before clicking Generate.
- For Kling 2.5 specifically, re-check resolution after selecting the model. If the UI lands on a paid/non-Unlimited resolution (for example 1080 with pricing), switch to an Unlimited-supported resolution before submitting.
- When `Create video` from an image opens the Video Generator, confirm the image actually populated the Start image slot before editing prompts or submitting.
- If selecting an existing creation exposes an `Apply` step, verify that the left `Start image` slot truly changed; do not assume `Apply` succeeded just because the picker closed.
- For long Magnific runs with repeated waits/retries, prefer moving the task into Hermes background execution and expose Hermes dashboard access when the user wants live progress instead of stopping to post incremental summaries.
- **Gateway-independent requirement for this user:** long Magnific background runs must be launched outside the Telegram gateway process tree so `/restart` or `hermes gateway restart` does not kill them. Use an OS-level service runner such as `systemd-run` or the helper pattern in `references/gateway-independent-magnific-runs.md` rather than the gateway-bound terminal background process manager.
- Pin the model/provider per long job. If the user changes the plan or says to use a different LLM model, stop or supersede the old independent job and start a new one with explicit `--provider` and `-m` flags; do not rely on whatever model the live chat is using.
- For gateway-independent background Magnific/video jobs, avoid approval-prompt stalls. Launch with the appropriate noninteractive approval mode (for the current helper, `--yolo`) or pre-approve required browser/terminal actions, because an unattended systemd task can otherwise exit early when a tool asks for confirmation.
- When handing a Magnific run to Hermes background, tell the user exactly where to monitor it: in Hermes dashboard, background runs appear primarily as separate entries in **Sessions** (usually the newest session), not always as a dedicated big "background jobs" panel. For gateway-independent systemd jobs, also give the unit name and log path.
- If you expose the dashboard through a public tunnel, treat the URL as volatile and update the user if the tunnel rotates to a new hostname.
- For long Magnific runs with repeated waits/retries, prefer moving the task into Hermes background execution and expose Hermes dashboard access when the user wants live progress instead of stopping to post incremental summaries.
- If the user asks for remote dashboard access, prefer a more stable public dashboard tunnel over ad-hoc rotating links when possible, and surface the live dashboard URL clearly.
- **Interrupted/timed-out continuation discipline:** when the user asks to continue an interrupted or timed-out Magnific/video background task, do not blindly relaunch generation. First audit the independent-task logs, current project files, final outputs, and media integrity. If the previous worker already completed, verify dimensions/duration/silence/audit notes and deliver the completed media instead of starting a duplicate run. Relaunch only when the audit proves the requested deliverable is incomplete or stale.
- Support file: `references/magnific-unlimited-and-queue-rules.md` captures the session-tested queue/verification rules.

## Timing sync and text-to-video discipline

- If the user says the script, voiceover, and scenes are not aligned, treat that as a full workflow correction, not a cosmetic note.
- Rebuild the project from a timing-first plan:
  1. write or rewrite the narration as shot-sized beats,
  2. map each beat to the model's actual available duration options,
  3. if a beat does not fit an available duration, rewrite the beat before generation,
  4. only then generate the replacement clips.
- Do not keep a 7-second narration beat and silently generate a 10-second clip unless the narration and scene were explicitly rewritten for that 10-second timing.
- If the user rejects the prior cut for script/scene mismatch, treat the old cut as obsolete and regenerate from scratch rather than trying to salvage the mis-synced sequence.

## Rejection recovery: consistency, pacing, and reel framing

- If the user rejects a short because the protagonist or environment drifts between clips, switch immediately from a text-only bias to a **consistency-first** workflow: lock one character bible, one environment bible, and use clean start/reference images whenever that is the most reliable path.
- For continuity-heavy shorts, define the protagonist in one durable spec before generation: age range, hair, clothing, face shape, palette, and any role markers (for example nurse scrubs). Reuse that exact spec in every prompt.
- Keep one spatial bible for the location as well: the same door, hallway palette, kitchen, bedroom threshold, and lighting logic must recur across clips unless the story explicitly changes them.
- When the user asks for a Reel/TikTok/Short, verify that the generated clips themselves are composed as native-feeling **9:16** shots. Do not accept a workflow that produces landscape clips and then fakes vertical with blurred side-fill or background duplication.
- If source clips arrive in landscape or otherwise fail to feel like native short-form framing, reject or regenerate them; do not treat blurred-background vertical wrapping as an acceptable final delivery.
- When a user complains about dead air, audit narration pacing as a production problem, not just a mixing tweak: shorten the script if needed, tighten pauses aggressively, and prefer a shorter stronger cut over preserving a sluggish runtime.
- In short-form horror/suspense work, every shot must either advance story or escalate tension. Remove passive filler beats instead of trying to cover them with music.

## Direct text-to-video constraint handling

- If the user explicitly requires direct text-to-video with no start frame, verify that the chosen model and current Magnific UI truly allow Generate with an empty start/reference slot.
- If the approved model keeps Generate disabled until Start is populated, do not bypass the user's rule by sneaking in a reference image.
- In that case, stop and report the exact product constraint: which approved models still require Start / Start-End in the current UI, and that true text-only submission was blocked.
- If the user then changes the model choice (for example from a Fast variant to the Standard variant), cancel the superseded background run and restart with the latest model instruction rather than trying to continue the stale run.

## Final delivery discipline for chat platforms

- Do not answer a media-delivery request with only a local file path when the platform can accept native media.
- For Telegram delivery, actually send the file as media.
- If the original export is too large for the bot/platform limit, create a smaller watchable delivery copy and send that version instead of replying with only the filesystem path.

## Brand-site reference vs footage-source discipline

When remaking a branded teaser or ad for this user, distinguish **brand research** from **footage sourcing** explicitly:
1. If the user says to use Magnific stock/generated clips, do **not** use the brand website's hero videos, product videos, stills, background images, or downloaded visual sections as main footage.
2. Use the brand website only for tone, copy, logo, palette, and positioning unless the user explicitly asks to reuse website media.
3. The official logo may be used for a local outro, but preserve it exactly with local motion graphics rather than AI-generating a distorted logo.
4. Start a clean project/version directory for the remake and prohibit reuse of the prior final export or its source clips.
5. Write source provenance into the audit summary for every clip: Magnific stock, Magnific generated, local motion graphics, or other allowed source.
6. Before final delivery, verify the audit states that no website footage was used when that was the user's correction.
7. For landscape/high-quality corrections after a rejected preview-watermarked or portrait/reel cut, use a fresh landscape project directory, render 16:9 master and delivery copies, and explicitly reject any asset URL or file path containing preview/watermark markers such as `/previews/`, `magnific_watermarked`, `watermarked`, or low-res thumbnail names.
8. For Magnific stock downloads, prefer the visible account UI's original/1080p download controls from the logged-in CDP browser. If the browser download path does not receive a file, inspect page fetch/XHR activity or the download API response, but do not persist signed URLs/tokens in notes, scripts, audit summaries, or final messages.
9. Audit final branded teasers with both metadata and visual sampling: ffprobe final dimensions/duration/codec/bitrate, create sampled frames from the final render, visually inspect them for Magnific/Freepik/preview watermarks and portrait/side-fill artifacts, then record the result in `notes/audit_summary.md`.
7. **Preview/watermark rejection rule:** if a branded commercial/real-estate video is meant for final client use, never use Magnific/Freepik stock search previews, thumbnails, or preview MP4s as final footage. Use logged-in original downloads, licensed stock downloads, or clean generated exports only; inspect every clip for visible watermarks before assembly.
8. **Aspect-ratio correction rule:** when the user explicitly asks for landscape, do not reuse or adapt a 9:16 reel workflow. Start a clean landscape project, target 16:9 (prefer 1920x1080), and verify both master and delivery copy dimensions before final response.
9. For session-tested details, see `references/branded-real-estate-landscape-no-watermark.md`.

- The `Start image` slot is mandatory for this workflow and may appear empty even when a previous generation card was selected elsewhere; verify the left-side slot itself.
- A bad framed or nested-screen reference image contaminates downstream clips. Swap it immediately rather than trying to fix the result in prompting alone.
- `Generate Unlimited` can appear only after the correct reference/model combination is valid; if it is missing or disabled, re-check the left form rather than the gallery.
- Capacity failures on one model are a routing problem, not a story-planning problem. Switch to another Unlimited model and keep the shot order intact.
- Keep per-project notes of: preferred clean reference frame, usable unlimited fallback models, known bad framed images, and the exact shot list already queued.

## Consistency-first recovery after rejection

When the user rejects a Magnific short for **character drift, scene drift, dead pacing, or fake vertical framing**, treat that as a workflow correction, not a cosmetic tweak. See `references/consistency-first-rebuild-notes.md` for a compact session-tested playbook.

Recovery rules:
1. **Character continuity beats text-only purity.** If direct text-to-video is causing the lead character to change face, hair, clothing, or age across shots, switch to a consistency-first workflow with clean reference/start images. For this user, once continuity breaks, preserving the same protagonist matters more than preserving a no-reference rule.
2. **Do not solve drift with longer prompts alone.** AI video tools often lack persistent cross-clip character memory; when identity drift appears, improve the reference/start-image structure first, then tighten prompt wording.
3. **Lock an appearance bible before regenerating.** Write one compact description for the protagonist and reuse it in every prompt: same age range, skin tone, hair color/style, clothing silhouette, facial structure, distinctive markers, and recurring props.
4. **Lock the apartment geography too.** Reuse the same front door, hallway palette, kitchen look, and bedroom threshold language across all clips. Do not allow the environment to redesign itself shot-to-shot.
5. **Minimize location changes in the redo.** If the previous cut drifted between rooms, simplify the story geography and keep more shots in the same corridor/room unless the location change is essential to the plot.
6. **Shorten the cut instead of defending dead space.** If the current version feels padded, rewrite the script into a punchier 30-40 second structure with a hook in the first 1-2 seconds and no passive bridge shots.
7. **Tighten narration aggressively.** Audit the voice track for multi-second silence; if there are long gaps, regenerate or trim the VO before final export. Do not leave long dead-air pauses between lines just because the clip plan was longer.

## Native reel framing verification

Do not assume the final piece is a proper Reel just because the export file is 9:16.

Before final delivery:
1. Verify the generated source clips themselves are suitable for vertical short-form composition.
2. If the downloaded clips are actually landscape footage placed into a portrait wrapper, reject that output path.
3. Do **not** use blurred-background side fill or landscape-in-portrait padding as the main rescue strategy for a Reel/TikTok/Shorts deliverable.
4. Prefer one of these instead:
   - regenerate with truly usable vertical composition,
   - switch to a model/settings path that produces better native short-form framing,
   - or use an intentional crop/reframe that still looks native and keeps the subject dominant in frame.
5. Final acceptance check: the result should feel like a natively composed vertical social video, not a horizontal clip adapted after the fact.

## Pitfalls

### 1. Assuming one Magnific generation can produce a full 45–90 second anime short
It usually cannot under the best unlimited anime-friendly model. Plan for multi-clip assembly.

### 2. Staying on `Auto` when the user explicitly asked for the best unlimited model
If the user says to inspect all models, do not leave it on `Auto`.

### 3. Forgetting to switch to Unlimited-compatible settings
After selecting Kling 2.5, the UI may show that the current resolution is not supported by Unlimited. Use the UI control to switch to Unlimited mode.

### 4. Starting without a reference image when consistency matters
For anime protagonist continuity, starting from a strong image and then using `Create video` is better than pure text-only clip generation.

### 5. Reusing a bad reference image
If the selected `Start image` already contains a visible screen, frame border, picture-in-picture composition, or other nested-image artifact, later clips inherit that mistake and the whole short looks fake or "video inside a frame." Before generating follow-on clips, reopen the picker and swap to a clean portrait/reference frame.

### 6. Capacity modal on Kling 2.5 Unlimited
A temporary full-capacity modal is not a permanent blocker. Close it, wait the amount of time the UI requests when provided, retry the same clip automatically, and keep already queued clips in place.

### 7. Regenerating references when good ones already exist
Do not regenerate references in bulk if usable frames are already available in the project. Audit existing frames first, reuse the best one for each clip, and only regenerate the exact weak or missing frame.

### 8. Delaying quality fixes until the end
Make each frame acceptable at the point it is created. If a frame looks wrong, retry immediately right there instead of postponing cleanup until the end of the project.

### 9. Knowing when to stop retrying saturation
Keep working through temporary limit/capacity messages. Only stop and report a blocking capacity issue after more than 45 continuous minutes without successfully starting any new video generation.

## Suggested shot architecture for anime crime-thriller shorts

For a 45–90 second short:
1. Hook: impossible reveal in first 1–3 seconds.
2. Clue montage: 2–3 short shots.
3. Victim/danger beat.
4. Chase beat.
5. Twist reveal.
6. Final page / final line / cliffhanger.

## Deliverables checklist

- Script saved to a text file.
- Detailed JSON-style prompt plan saved to a file.
- Andrew voiceover rendered and merged.
- Magnific clips generated from the selected model.
- Final edited MP4 exported.
- If delivering through chat platforms, verify the final file is actually watchable in-platform.
  - If the platform rejects the original export as too large, create a delivery copy at a smaller bitrate/resolution and send that version instead of replying with only a filesystem path.

## References

- `references/model-selection-and-assembly-notes.md` — observed model notes, unlimited-mode findings, and assembly guidance from a live Magnific workflow.
- `references/magnific-live-ops-notes.md` — compact operating checklist for sequencing frames before videos, verifying settings before every generate click, choosing clean references, and switching to another Unlimited model when the current one is saturated.
- `references/gateway-independent-magnific-runs.md` — systemd-based pattern for long Magnific jobs that must survive Telegram gateway restarts and use a pinned per-job LLM model.
- `references/consistency-first-rebuild-notes.md` — corrective workflow for rejected AI-video shorts with character drift, scene drift, dead-air pacing, or fake vertical framing.
- `references/brochure-driven-real-estate-teasers.md` — brochure/PDF-driven luxury real-estate teaser workflow: extract project facts, choose location-correct no-watermark stock, preserve exact logos, avoid floor plans, and audit final landscape deliverables.
