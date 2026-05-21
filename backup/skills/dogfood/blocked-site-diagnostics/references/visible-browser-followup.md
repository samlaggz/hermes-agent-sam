# Visible browser follow-up for blocked-site investigations

Use this when the built-in browser or cloud browser hits a block, but the user still needs a human-visible session for legitimate login, manual verification, or evidence gathering.

## When this pattern fits

- The normal browser tool gets a 403/security-filter page before login.
- The user wants a watchable session or needs to provide a one-time verification code.
- Cloud browser/session providers are unavailable, blocked, or not funded.
- The goal is not silent evasion; the goal is a visible, user-observable browser that can be manually verified.

## Practical local live-view recipe

1. Run a desktop on a virtual display:
   - `Xvfb`
   - lightweight WM like `fluxbox`
2. Expose the desktop through VNC:
   - `x11vnc`
3. Publish it in a browser-friendly way:
   - `novnc` + `websockify`
4. Share it externally:
   - reverse tunnel such as `ssh -R 80:localhost:6080 nokey@localhost.run`
5. Launch a real browser in that display:
   - Playwright-installed Chromium worked well in this session.

Useful apt packages on Debian-like hosts:
- `x11vnc`
- `fluxbox`
- `novnc`
- `websockify`
- `xdotool`

## Why this helps

- The user can watch the session live.
- Human verification steps stay observable.
- The site is being used through a normal visible browser session rather than opaque background automation.
- You can still collect screenshots and classify the original block separately.

## GUI automation fallback pattern

When DOM/browser-level control is unreliable in the visible desktop session:

- capture the X display with `ffmpeg -f x11grab ... -frames:v 1 ...`
- inspect screenshots with vision tooling
- click/type via `xdotool`
- repeat in short verify-after-each-action loops

This is useful for:
- top-right login buttons
- modal dialogs
- one-time email code forms
- flows where the built-in browser snapshot is unavailable or blocked

### Credential + verification timing rules

For user-visible login flows in a shared live browser session:

- only ask for the password once the password field is confirmed visible and focused; do not ask early
- when the next step requires the user to act (password, OTP, device approval, alternate method), prefer a `clarify` prompt with explicit button choices instead of a vague free-form ask
- keep the live-view URL stable while waiting for user input so they can watch the same session

### OTP / multi-box input pitfall

Some verification UIs silently drop the first digit or move focus unpredictably when driven through desktop automation.

Use this pattern:

1. type the full code once
2. verify the visible state with a fresh screenshot before assuming success
3. if the code is rejected and the site offers a resend flow, prefer `Send again` over repeatedly retrying the stale code
4. after resending, treat the previous code as invalid unless the user explicitly confirms otherwise

## Guardrails

- Keep the diagnostic and the follow-up distinct.
- Do not describe this as a bypass technique.
- If the site still presents CAPTCHA or explicit anti-bot verification, stop and let the user complete it manually.
- Prefer user-visible/manual completion over repeated retries from the blocked automation path.

## Operational notes learned here

- Some browser-cloud MCP setups can be correctly configured yet still unusable because the provider account lacks balance. Treat that as a provider/billing issue, not an integration failure.
- For Browser Use MCP specifically, Hermes may need a full process restart before newly added MCP servers become callable in-session.
- If the user wants the browser session to remain watchable during login, keep the noVNC URL stable and avoid replacing it with a non-visible automation path mid-task.
