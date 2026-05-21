# Shared live CDP browser workflow for Magnific + Google login

Use this reference when a session needs one browser that is both:
- **watchable by the user** via noVNC/live URL, and
- **reused by Hermes browser tools** for non-GUI operations.

## Durable lesson from the session

The reliable pattern was to stop treating the visible browser and Hermes browser tools as separate worlds. Instead:
1. start a self-hosted visible Chromium session
2. expose it with noVNC for the user
3. launch Chromium with a fixed remote-debugging port
4. point Hermes `browser.cdp_url` at that port
5. use the same browser state for GUI watching and non-GUI browser actions

This avoided the earlier split where the visible session worked but the normal browser tool path still hit blocked/403 behavior.

## Working recipe

### 1) Visible browser stack
- Xvfb on `:99`
- fluxbox
- x11vnc on `5900`
- noVNC/websockify on `6080`
- reverse tunnel to localhost.run for a public watch URL

Viewer URL shape:

```text
https://<random-subdomain>.lhr.life/vnc_lite.html?autoconnect=1&resize=remote&path=websockify
```

### 2) Chromium with stable CDP
Launch Chromium with a persistent user-data-dir and fixed debugging port:

```bash
/usr/bin/chromium \
  --user-data-dir=/tmp/hermes-live-browser-profile \
  --remote-debugging-address=127.0.0.1 \
  --remote-debugging-port=9222 \
  --no-sandbox \
  --no-first-run \
  --no-default-browser-check \
  --disable-session-crashed-bubble \
  --disable-infobars \
  --start-maximized \
  https://www.magnific.com
```

Then verify:

```bash
curl http://127.0.0.1:9222/json/version
```

Expected signal: `webSocketDebuggerUrl` is present.

### 3) Persist Hermes browser config
Set Hermes to attach to that browser by default:

```bash
hermes config set browser.cdp_url http://127.0.0.1:9222
hermes config set browser.engine chrome
hermes config set browser.command_timeout 60
```

Effect: normal Hermes browser tools can reuse the same live browser session instead of spawning a separate local path.

## Why this matters

When the user asks for a live browser they can watch **and** wants later non-GUI browser operations to behave the same way, the skill should prefer a shared CDP-backed browser. The non-GUI tool calls then inherit:
- the same cookies/session state
- the same visible page state
- the same site reputation / browser identity path

## Workflow preference learned from the user

For this user, browser tasks should prefer:
- self-hosted watchable sessions
- the same live browser for GUI and non-GUI steps when possible
- asking for passwords only when the password prompt is actually on screen
- clarifying target service quickly if the user says "login this email" and there are multiple possible sites in play (for example Magnific vs Gmail)

## Login-flow pitfall

A real pitfall from the session: do not assume that an email supplied during a site workflow belongs to the current site. If the user says "login this email on Gmail," switch the live session to Google sign-in immediately rather than continuing inside the current site login form.

## Magnific-specific outcome

Using the shared CDP browser made `browser_navigate("https://www.magnific.com")` succeed through the normal Hermes browser tool path after direct local attempts had previously hit a block page.

## Suggested trigger for future sessions

Use this pattern whenever the user asks for any combination of:
- "live session"
- "share the link"
- "watch browser live"
- "use the same browser for normal browser operations too"
- login flows where the user wants to watch each step
