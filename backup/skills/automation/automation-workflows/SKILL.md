---
name: automation-workflows
description: Skills for orchestrating complex task sequences, environment setups, and multi-step workflows.
---

# Automation Workflows

Use this skill to manage structured execution paths when a task requires multiple phases (e.g., setup -> integrate -> test).

## Workflow Patterns

### 1. The "Silent Integration" Pattern
When the user requests an integration that should be "silent" or "default" (like CloakBrowser with Playwright):
- **Analyze**: Inspect the source code of the tool being integrated.
- **Hook**: Find the entry point where it can be injected into the host environment (e.g., custom drivers, env vars, or wrapper classes).
- **Verify**: Create a minimal test script that uses the standard interface but triggers the integrated logic.

### 2. The "Gateway-Independent Background Task" Pattern
Use when a long-running Hermes task must survive gateway restarts, model switches, or chat reconnects.
- **Do not attach durable work to the gateway process tree**: gateway-bound background processes can die when `hermes gateway restart` is used to pick up config/model changes.
- **Launch as an OS-managed service**: use `systemd-run` (or an equivalent supervisor) so the task has its own lifecycle, logs, and status independent of Telegram/gateway.
- **Pin the model per job**: pass `--provider` and `-m/--model` explicitly for each long task so plan changes can run on a different LLM without changing the live chat model.
- **Treat plan/model changes as process boundaries**: stop obsolete units or start a replacement unit that resumes from the saved session/project files with the new provider/model.
- **Keep logs and handles**: report the systemd unit name and log path, then verify with `systemctl status` rather than assuming the task is still alive.
- **Reference**: See `references/gateway-independent-hermes-tasks.md` for a reusable systemd-run recipe and the local helper script path used in this environment.

### 3. The "Visible Browser + Public Watch URL" Pattern
Use when the user wants to watch a browser session live, especially for login/verification flows where cloud browser products are unavailable or undesirable.
- **Build a local GUI stack**: Start a virtual desktop (`Xvfb`), a lightweight window manager (for example `fluxbox`), a VNC server (`x11vnc`), and a web VNC bridge (`noVNC`/`websockify`).
- **Expose it**: Publish the noVNC port with a temporary tunnel such as reverse SSH via `localhost.run` or an equivalent tunneling service.
- **Verify the watch URL**: Confirm the public URL returns HTTP 200 before handing it to the user.
- **Keep the browser in that display**: Launch Chromium/Playwright with `DISPLAY=:99` (or the chosen display) so every interaction is visible in the live view.
- **Automate carefully**: For OTP/login screens with fragile focus handling, prefer slower, verifiable input steps and screenshot checks between actions.
- **Pause exactly at credential checkpoints**: when the user wants to supply secrets manually, stop only when the password, OTP, push-approval, or recovery prompt is actually on screen; after the user confirms completion, immediately inspect the new state and continue without making them restate context.
- **Preserve continuity**: Keep the stack alive across pauses so the user can watch, intervene, or provide fresh verification codes without rebuilding the environment.
- **Choose the right browser for login-sensitive sites**: if a site rejects an automation-oriented browser build as insecure, retry the same visible session with a mainstream system browser profile before assuming the login itself is blocked.
- **For Gmail / webmail follow-up work, prefer direct mailbox routes after login**: once authentication succeeds, navigate explicitly to stable URLs like `https://mail.google.com/mail/u/0/#inbox` or `#search/<query>` instead of relying on keyboard shortcuts alone. Search-result pages can keep focus in the search box or ignore single-key navigation, so direct hash routes are more reliable in a watched Xvfb/VNC session.
- **When the user asks to 'check mail,' report only what is visibly grounded**: summarize the top visible senders, subjects/snippets, and dates/times from the inbox or search results, and clearly separate visible facts from any broader inference about totals or account activity.
- **Reference**: See `references/visible-browser-liveview.md` for a reusable minimal stack and validation checklist, and `references/google-login-visible-browser.md` for Google/Gmail-specific login handoff notes.

### 4. The "Sourced-Media Assembly" Pattern
Use when a user asks for a finished promo/video, not just a plan.
- **Inspect the target creation app first**: Identify whether the web app already has native tools for video, audio, voice, stock, and project editing before building an external pipeline.
- **Source legally reusable media**: Prefer royalty-free footage/music/SFX with direct, scriptable downloads and save a credits/source manifest alongside outputs.
- **Generate the deliverables, not just prompts**: If the user asks to "make the video," produce the rendered file plus script/asset notes, rather than stopping at concept copy.
- **Verify the render visually**: Export at least a contact sheet or representative frames and inspect for text placement, cropping, and general polish.
- **If the user rejects the first creative pass, rebuild instead of lightly tweaking**: treat the correction as a style reset. Re-anchor on reference brands/examples, replace weak or repetitive clips, and change pacing/typography/music strategy rather than only swapping headlines.
- **For premium real-estate/luxury promos, search broader lifestyle + amenity terms**: include not just skyline/building terms but also lobby, concierge, pool, rooftop lounge, spa, gym, landscaped family walking, elegant women in interiors, and architectural details so the cut sells both the property and the feeling of living there.
- **Before delivery, make a compatibility pass for phones and messaging apps**: inspect the export with `ffprobe` and do not assume an `.mp4` container is enough. If the video stream is H.264 4:4:4 / `yuv444p` (or another niche profile), create a delivery copy as H.264 High + `yuv420p`, AAC audio, and `+faststart` so Telegram/WhatsApp/mobile players can open it reliably. Keep the higher-fidelity master separately if needed.
- **For current-events explainers and infographic videos, ground every claim in fresh open reporting before scripting**: pull a small set of reputable recent sources, keep the voiceover tightly scoped to what those sources support, and save a concise `sources_and_script.md` alongside the render so future revisions can trace each claim back to the reporting reviewed that day.
- **For text-heavy infographic slides, verify legibility from exported frames, not just source stills**: long bullets that fit in the design file can clip after render-time motion or scaling. Prefer shorter rewrite passes over shrinking text, and if a Ken Burns / zoom treatment harms readability, switch to static slides plus clean crossfades.
- **Match the handoff to the user's workflow preference**: when a long creative task is interrupted or hits a system limit, end with tappable next-step choices (for example Continue / Retry / Summarize / Stop) whenever the platform supports it, instead of only a plain-text status dump.
- **Reference**: see `references/phone-safe-video-delivery.md` for a minimal compatibility checklist and a known-good ffmpeg re-encode recipe.

#### Premium real-estate / developer-style branch
Use this branch when the user wants a luxury property film rather than a generic promo.
- **Do not default to voiceover** unless the user asks for it. A frequent preference for premium developer-style ads is *music-only* with sparse, elegant messaging.
- **Prefer brand-film pacing over explainer pacing**: slower, more deliberate hero shots; restrained text; less sales copy; fewer but stronger clips.
- **Prioritize clip mix intentionally**: exterior hero architecture, lobby/arrival, concierge/service, rooftop/pool/wellness amenities, architectural details, women/family lifestyle moments, then a closing skyline/exterior beat.
- **Cull weak or repetitive clips aggressively**: if a clip feels generic, duplicated, or not visibly premium, replace it instead of padding the runtime.
- **Match transitions to the music structure**: smooth dissolves or clean cuts for most transitions, with occasional short black-frame / flash-cut accents only on stronger beats and never overused.
- **Upgrade typography deliberately**: serif headline + modern sans support text works well for premium real-estate edits; use hierarchy, spacing, and restrained placement instead of default centered captions everywhere.
- **Treat lifestyle as part of the sell**: if the user asks for property *and* feeling, ensure people enjoying the amenities are present, not just empty architecture.
- **Reference**: see `references/magnific-premium-stock-sourcing.md` for Magnific-specific search keywords, download behavior, and clip-selection heuristics.

## Pitfalls
- **Pollution**: Avoid creating cluttered directories for one-off tasks; use subdirectories if necessary to maintain clean roots.
- **Silent Failures**: If an integration is meant to be "silent," ensure it doesn't break existing CLI output or environment variables unless intended.
- **Gateway-bound long jobs**: Do not use a gateway-owned background process for work that must survive `/restart`, provider changes, or Telegram reconnects. Use an independent service and pin its provider/model.
- **Unverified background survival**: After a restart, check `systemctl status hermes-task-*` or the helper's `list/status` command before telling the user a task is still running.
- **Unverified visibility**: Do not assume a tunnel or noVNC stack works just because the processes started; verify the public watch URL before telling the user to use it.
- **Fragile OTP entry**: Multi-box verification UIs may drop the first digit or lose focus under automation. Add intermediate screenshot/state checks instead of blindly retrying codes.
- **Half-finished creative workflows**: When the user asked for a real video, stopping after writing the script or gathering assets is incomplete. Finish with an actual render and supporting files.
