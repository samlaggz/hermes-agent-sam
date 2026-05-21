---
name: magnific-creative-workflows
description: Use Magnific for image/video generation and downloads with a shared live browser session, login checks, prompt discipline, and copyright-safe creative workflows.
version: 0.1.0
author: <REDACTED_PUBLIC_BACKUP>
license: MIT
metadata:
  hermes:
    tags: [magnific, browser, image-generation, video-generation, prompts, copyright, shorts]
---

# Magnific Creative Workflows

Use this skill when the task involves **Magnific** for:
- generating images or video
- downloading stock or generated assets
- building short-form creative content from Magnific outputs
- running a watchable live browser session while Hermes also uses non-GUI browser tools

## Core rule

**Before generating, downloading, or exporting anything from Magnific, verify login state first.**

If Magnific is not logged in:
1. open the Magnific login flow in the active shared browser session
2. use the user-provided Magnific account for the current engagement
3. never persist passwords or other secrets in the skill or memory
4. if a CAPTCHA or anti-bot challenge appears, pause and ask the user to complete it manually before continuing

Do not assume that arriving at `/app/...` means the account is authenticated enough for generation or downloads. Check the visible auth state first.

## Shared-browser rule

Prefer a **single shared live Chromium/CDP session** for both:
- watchable GUI browsing the user can inspect live
- Hermes non-GUI browser operations (`browser_navigate`, `browser_click`, `browser_console`, screenshots)

This avoids split-state bugs where the visible browser and the automation browser disagree about login or page state.

## Magnific workflow

1. Confirm the shared browser session is alive.
2. Navigate to the exact Magnific tool needed.
3. Check whether the page shows authenticated app controls or a logged-out header.
4. If logged out, complete login before generating or downloading.
5. Only after auth is confirmed, proceed with prompts, generation, asset review, and export.
6. If login required a redirect, CAPTCHA handoff, or OTP verification, assume the working prompt/editor state may have been lost and re-open the target generator page before continuing.
7. Re-inject or re-validate the prompt after login before clicking Generate.
8. Re-check auth before each new generation or download batch if the session may have drifted.

## Prompting rule for generated visuals

When using Magnific for stylized content, prefer **structured prompt payloads** over loose one-line prompts.

Recommended structure:
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

This is especially useful for multi-scene shorts where consistency matters.

## Anime-inspired shorts workflow

For anime-style shorts, default to:
- **original anime-inspired characters and settings only**
- **9:16 vertical composition**
- **hook in the first 1–2 seconds**
- a visual story built around 3–5 key images max
- high-contrast readable compositions that survive phone viewing

### Suggested short structure
1. **Hook frame** — a high-tension or curiosity-driving first image
2. **Escalation** — reveal the threat, mystery, or emotional stakes
3. **Turn** — a surprising visual beat or reversal
4. **Payoff / cliffhanger** — end on a punchy final image or line

## Video-generator model selection inside Magnific

When the user asks for the **best unlimited model**, inspect the live model list rather than guessing from memory.

Selection order:
1. supports the requested style
2. supports the requested aspect ratio / duration behavior
3. is available under the user's current account constraints
4. is explicitly marked **Unlimited** if unlimited generation is requested

### Proven model choice for anime-style vertical shorts
For anime / illustration-heavy short-form video, a durable observed choice was:
- **Kling 2.5** when the constraint was **best Unlimited + Illustration & animation support**

Why this mattered:
- it matched the requested anime-inspired visual direction better than purely realistic unlimited options
- it supported the vertical short workflow
- but it still behaved like a **short-clip generator**, not a full 45–90 second one-shot narrative generator

## Unlimited-mode pitfall in Magnific Video Generator

A recurring pitfall: the selected model can be valid, but the current resolution or entry path may not yet be in the app's **Unlimited** mode.

If Magnific shows a message like:
- current resolution not supported by Unlimited
- switch to Unlimited mode

then do this:
1. create/open the video workflow from the selected still or asset
2. switch the model first
3. click the in-app control to **Switch to Unlimited mode**
4. verify the UI now says the current resolution is covered by Unlimited
5. only then generate

## Long-form short creation from clip-limited models

If the user wants a **45–90 second** anime short, do not promise that Magnific alone will produce the whole piece in one render.

Preferred workflow:
1. generate a strong anchor image or keyframe in Magnific
2. create one or more short video clips from that image or related assets
3. repeat for major story beats
4. download the clips / key assets
5. assemble the final short locally with voiceover, captions, pacing, and music/SFX

This is the right fallback when the best unlimited anime-capable model is clip-oriented rather than long-form.

## From-image video workflow

When a good image result already exists in the Magnific results pane:
1. use the card's **Create video** action instead of rebuilding from scratch
2. confirm the image is attached as the **Start image** in Video Generator
3. switch model / aspect ratio / duration after the image is attached
4. then inject the structured prompt and generate

## Copyright guardrails

For anime-style content on YouTube or social platforms:
- do **not** recreate named copyrighted anime characters too closely
- do **not** use franchise logos, exact costumes, signature props, or recognizable scene copies
- do **not** reuse copyrighted soundtrack audio without permission
- prefer **original IP** that borrows broad genre language rather than protected character identity

The safest path is "anime-inspired" rather than "fan recreation."

## CAPTCHA / anti-bot handling

If Magnific login shows reCAPTCHA, Turnstile, or another challenge:
- stop normal automation
- keep the live view open
- tell the user exactly what must be completed manually
- resume only after the user confirms it is done

## Email + OTP login handoff

Magnific may allow the email/password step and then require a 6-digit email verification code.

When that happens:
- keep the shared live browser/CDP session open instead of switching browsers
- let the user provide the fresh code in-chat for the current session only
- enter the OTP in the same browser state that received the login redirect
- after successful verification, navigate back to the exact generator/download surface you need and confirm the logged-in controls are visible before proceeding
- never store the OTP, password, or full credential set in skills or memory

This pattern matters because generation pages often clear or reset their editor state during auth handoff.

## Output guidance

For Shorts / Reels / TikTok style exports:
- aspect ratio: `9:16`
- keep key text centered and mobile-safe
- use quick pacing
- prefer short dramatic lines over dense exposition
- export MP4 with broad phone compatibility
- when rendering outside Magnific, prefer H.264 MP4 with `yuv420p` and `+faststart`; if a first render lands on `yuvj420p`, consider a final compatibility re-encode before delivery
- if Andrew voice is requested and a long one-shot TTS call is flaky, generate **chunked Andrew narration and merge it** before final assembly

## References

- `references/anime-shorts-and-magnific-notes.md` — distilled notes on viral short structure, YouTube discovery signals, copyright boundaries, and Magnific login/generation workflow.
- `references/magnific-login-and-anime-short-session-notes.md` — durable notes on shared-CDP login handoff, OTP recovery, prompt re-injection after auth, and anime-short assembly flow.
- `references/magnific-unlimited-video-model-notes.md` — observed model-selection and unlimited-mode behavior for Magnific Video Generator, including clip-limited long-form assembly strategy.

## Pitfalls

1. Generating while logged out and only noticing at download time.
2. Using a different hidden browser than the live browser and losing auth state.
3. Overly loose prompts that produce inconsistent multi-scene characters.
4. Making anime visuals too derivative of a known franchise.
5. Trying to automate through CAPTCHA instead of pausing for manual completion.
6. Assuming the prompt box still contains the intended text after login/OTP handoff.
7. Delivering a short without checking final phone-compatibility details like pixel format and `+faststart`.
