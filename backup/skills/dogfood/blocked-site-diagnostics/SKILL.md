---
name: blocked-site-diagnostics
description: Use when a website blocks access, serves 403/429/security interstitials, or behaves differently in automation. Diagnose the likely cause safely without attempting bypass.
version: 1.0.0
author: <REDACTED_PUBLIC_BACKUP>
license: MIT
metadata:
  hermes:
    tags: [browser, diagnostics, 403, 429, anti-bot, access]
    related_skills: [captcha-aware-browsing, hermes-agent]
---

# Blocked-Site Diagnostics

## Overview

Use this skill when a site returns blocked-access pages, anti-bot interstitials, 403/429 responses, suspicious redirect loops, empty pages, or automation-only failures.

This is a diagnostics skill, not a bypass skill. The goal is to identify what kind of blocking is happening, collect evidence, and recommend legitimate remediation.

## When to Use

- The browser lands on a 403, 429, access denied, or security filter page.
- A site works in a human browser but fails in automation.
- You see a CAPTCHA, interstitial, challenge, or verification step blocking access.
- The page content is missing, blank, looping, or replaced by a vendor-branded block page.
- Network or console behavior suggests blocked resources, failed auth, or rate limiting.

Do not use this skill to solve or bypass the block.

## Primary Workflow

1. Capture the visible state.
   - Use `browser_snapshot(full=true)` for visible text, titles, and interactive elements.
   - Use `browser_vision(question="Is this a blocked-access page, CAPTCHA, bot challenge, rate-limit page, or normal site error? Summarize the visible evidence.", annotate=true)` for visual-only interstitials.

2. Inspect runtime clues.
   - Use `browser_console()` to inspect JS errors, failed API calls, challenge scripts, and blocked assets.
   - If useful, evaluate targeted DOM expressions with `browser_console(expression=...)` for title, meta tags, body text fragments, and known vendor markers.

3. Classify the block.
   Common buckets:
   - CAPTCHA or anti-bot challenge
   - 403 forbidden / permission denied
   - 429 rate limit / too many requests
   - auth/session problem
   - geo/IP reputation or WAF decision
   - broken page unrelated to anti-bot

4. Collect evidence.
   Record:
   - page title
   - top visible error text
   - HTTP-like clues shown on page (403, 429, forbidden, unusual traffic)
   - vendor branding (Cloudflare, Akamai, PerimeterX/HUMAN, DataDome, Turnstile, reCAPTCHA, hCaptcha, GeeTest, Arkose)
   - reference ray/request/request-id values if visible
   - whether the problem appears before or after login

5. Recommend legitimate next steps.
   Choose from:
   - manual verification by the user
   - official API or export path
   - staging/test allowlist or disabling anti-bot in non-production
   - slower request cadence if rate-limited
   - checking auth/cookies/session expiry
   - checking region/IP reputation, VPN/proxy policy, ASN restrictions
   - asking site owner/admin for access or allowlisting
   - if the user wants to watch or complete the flow manually, pivot to a visible local browser session with a shareable live view rather than repeatedly hammering the blocked built-in browser; see `references/visible-browser-followup.md`
   - if the blocked task is a license/subscription/compliance question, separate what you can verify publicly (terms, legal pages, FAQ) from what requires the logged-in account UI (plan name, billing page, asset-specific license badges). State the verification boundary explicitly rather than over-claiming.

## Quick Triage Matrix

- CAPTCHA / challenge widget present
  - Report challenge type
  - Stop automation
  - If further diagnosis is needed, load or pivot to `captcha-aware-browsing`

- 403 page with security wording
  - Suspect WAF, bot score, IP reputation, or permissions
  - Report any visible reference ID and vendor branding

- 429 / too many requests
  - Suspect rate limiting
  - Recommend backing off, reducing concurrency, or using official APIs

- Login page loop or partial app shell
  - Suspect auth/session/cookie/storage issues
  - Inspect console and visible app state

- Blank page with console errors
  - Suspect broken app, CSP, script load failure, or blocked assets
  - Report the failed assets or JS exceptions

## Recognition Heuristics

Signals that usually indicate blocked access:

- Text like: access denied, forbidden, request blocked, unusual traffic, one more step, verify you are human, security filter, request didn't go through, too many requests.
- Visuals like challenge checkboxes, puzzle widgets, branded WAF pages, or verification overlays.
- Console clues like blocked XHR/fetch, 401/403/429 API calls, script load failures from challenge providers, or CSP violations.

## Reporting Template

- Detection: <blocked / not blocked / uncertain>
- Classification: <captcha | 403 security filter | 429 rate limit | auth issue | app failure>
- Evidence:
  - Title: <...>
  - Visible text: <...>
  - Vendor/reference: <...>
  - Console clues: <...>
- Action taken: Diagnosed only; no bypass attempted
- Suggested next step: <...>

## Integration with CAPTCHA-Aware Browsing

When the blocked page is specifically a CAPTCHA or challenge page:

- Treat `captcha-aware-browsing` as the first-response skill.
- Use this skill as the follow-up for deeper classification and remediation guidance.
- Keep the workflow defensive: detect, document, pause, and recommend.

## Requests to Use Stealth or Anti-Detect Tooling

If the user responds to a 403/challenge by asking to use stealth browsers, anti-detect wrappers, fingerprint spoofing, CAPTCHA-solving, or similar tooling to get through:

- Classify that as a bypass/evasion request, not normal diagnostics.
- Do not run or integrate the stealth tool against the protected target.
- It is acceptable to inspect the referenced tool or repo descriptively (for example, identifying that a browser project advertises stealth or fingerprint patching) when that helps explain why it is not appropriate for the blocked site task.
- Continue the blocked-site workflow instead: capture evidence, classify the likely block type, state clearly whether a CAPTCHA is actually present, and recommend legitimate next steps.

This matters because users often pivot from "diagnose the block" to "make the automation look human." The skill should keep the boundary explicit.

References:
- `references/visible-browser-followup.md` — when a blocked site task should pivot to a visible, user-watchable local browser session.
- `references/license-and-subscription-verification.md` — how to answer plan/license questions when public terms are reachable but logged-in account pages are blocked.
- `references/stealth-tool-escalation-example.md` — example of handling a user escalation from 403 diagnosis to anti-detect tooling.

## Common Pitfalls

1. Calling every 403 a CAPTCHA.
   - Some are permissions, expired sessions, region locks, or WAF decisions without a challenge.

2. Retrying blindly after a block.
   - Repeated retries can worsen throttling or reputation scoring.

3. Ignoring the console.
   - Many real clues live in failed requests, CSP errors, or auth failures.

4. Turning diagnosis into evasion.
   - Stay on evidence gathering and legitimate remediation only.

5. Overstating what was verified.
   - Public legal pages can answer some questions, but they do not prove the user's exact subscription tier or asset-specific stock rights. When account pages are blocked, distinguish "public terms say X" from "your plan page confirms Y".

## Verification Checklist

- [ ] Captured visible page evidence
- [ ] Inspected console/runtime clues when useful
- [ ] Classified the likely failure mode
- [ ] Did not attempt to bypass or solve protections
- [ ] Recommended a legitimate next step
