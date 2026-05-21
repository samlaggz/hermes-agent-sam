---
name: captcha-aware-browsing
description: Use when browser tasks may encounter CAPTCHA, bot-detection, or anti-automation interstitials. Detect the challenge, capture evidence, stop automation, and hand off safely instead of attempting to solve or bypass it.
version: 1.0.0
author: <REDACTED_PUBLIC_BACKUP>
license: MIT
metadata:
  hermes:
    tags: [browser, captcha, anti-bot, safety, escalation]
    related_skills: [blocked-site-diagnostics, hermes-agent]
---

# CAPTCHA-Aware Browsing

## Overview

Use this skill during browser automation when a site presents a CAPTCHA, bot check, security challenge, or similar anti-automation gate.

This skill is intentionally defensive: it helps detect and document the challenge, then pauses or redirects the workflow. It does not solve, bypass, defeat, or evade the protection.

## When to Use

- A page shows words like CAPTCHA, verify, challenge, security filter, access denied, unusual traffic, blocked, forbidden, or 403.
- The browser lands on a challenge page instead of the requested content.
- A widget such as reCAPTCHA, hCaptcha, Cloudflare Turnstile, slider, image grid, audio challenge, or puzzle appears.
- Console/network behavior suggests a challenge even if the DOM snapshot is incomplete.

Do not use this skill to automate solving or bypassing a challenge.

## Primary Workflow

1. Inspect the current page state.
   - Use `browser_snapshot(full=true)` when text content may reveal the challenge.
   - Use `browser_console()` to look for JS errors, blocked requests, or challenge-related messages.

2. Check for visual challenge indicators.
   - Use `browser_vision(question="Is there a CAPTCHA, bot challenge, security interstitial, or blocked-access page visible? Describe the evidence.", annotate=true)`.
   - Look for checkboxes, puzzle widgets, image grids, audio challenge controls, "verify you are human", 403/429, or branded anti-bot pages.

3. Automatic trigger behavior.
   - Treat any detected CAPTCHA or challenge page as an immediate trigger for this skill.
   - Pause the normal browsing objective and switch into detection/reporting mode.
   - If the page is more generally blocked, rate-limited, or access-denied beyond the challenge itself, pivot to `blocked-site-diagnostics` for deeper classification.

4. If a challenge is detected, stop normal automation.
   - Do not click through challenge widgets.
   - Do not attempt to interpret challenge prompts for the purpose of solving them.
   - Do not generate click coordinates, answers, or transcripts for completing the challenge.

5. Capture evidence for the user.
   - Report the exact visible message or page title.
   - Summarize the type of challenge (for example: reCAPTCHA checkbox, Cloudflare block page, 403 security filter, image challenge, audio challenge).
   - If available, mention any reference ID, status code, or vendor branding shown on page.

6. Offer safe next steps.
   - Ask the user to complete the challenge manually in their own browser session if appropriate.
   - Suggest using the site's official API, a whitelisted test environment, or permissions from the site owner.
   - For app QA, suggest disabling anti-bot controls in staging/test environments rather than trying to bypass them.
   - If the page is simply blocked, suggest checking IP reputation, login state, rate limits, headers, geofencing, or account permissions.
   - If diagnosis needs to go beyond the immediate challenge, load or pivot to `blocked-site-diagnostics`.

## Recognition Heuristics

Treat any of the following as likely challenge signals:

- Text: CAPTCHA, challenge, verify, blocked, forbidden, unusual traffic, one more step, security check, are you human, access denied.
- Status-like pages: 403, 429, permission denied, request didn't go through.
- Widgets: reCAPTCHA, hCaptcha, Turnstile, GeeTest, Arkose, slider puzzle, image selection grid, audio play button for verification.
- Redirect loops or blank content after navigation when a site normally has content.

## Reporting Template

Use a compact format like:

- Detection: Challenge detected / No challenge detected
- Type: <captcha/security interstitial/block page>
- Evidence: <title, on-page text, vendor, reference ID, console clue>
- Action taken: Paused automation and did not attempt to solve
- Suggested next step: <manual completion / official API / staging allowlist / investigate blocking>

## Safe Alternatives

When a challenge blocks the task, pivot to one of these instead:

- Manual handoff: user completes verification outside the automated flow.
- Official integration: API, export, webhook, or developer endpoint.
- Test-environment approach: disable or whitelist anti-bot controls in staging.
- Diagnostics: inspect headers, cookies, auth state, region/IP restrictions, and rate limiting.

## Common Pitfalls

1. Mistaking a 403 or security filter page for a normal navigation error.
   - Always inspect the visible page and title before retrying blindly.

2. Treating challenge analysis as permission to solve it.
   - Detection/documentation is allowed; generating the answer or interaction sequence is not.

3. Relying only on DOM text.
   - Some challenge widgets are mostly visual; use `browser_vision` as well.

4. Repeating requests aggressively after a block.
   - That can worsen rate limits or reputation issues. Pause and report instead.

## Verification Checklist

- [ ] Checked page text and/or title for challenge indicators
- [ ] Used visual inspection when the snapshot was insufficient
- [ ] Did not attempt to solve or bypass the challenge
- [ ] Reported evidence clearly to the user
- [ ] Offered a legitimate next step or diagnostic path
