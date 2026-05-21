# Live Browser Stack Reference

This reference captures a proven pattern for making a self-hosted visible Chromium session double as Hermes's default browser backend.

## Stack

- `Xvfb :99 -screen 0 1440x900x24 -ac +extension RANDR`
- `fluxbox`
- `x11vnc -display :99 -forever -shared -nopw -rfbport 5900`
- `/usr/share/novnc/utils/novnc_proxy --vnc localhost:5900 --listen 6080`

## Public watch URL pattern

Use a reverse tunnel such as:

```bash
ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=30 -o ExitOnForwardFailure=yes -R 80:localhost:6080 nokey@localhost.run
```

Viewer URL shape:

```text
https://<subdomain>.lhr.life/vnc_lite.html?autoconnect=1&resize=remote&path=websockify
```

Verify before sharing:

```bash
curl -I -L --max-time 20 'https://<subdomain>.lhr.life/vnc_lite.html?autoconnect=1&resize=remote&path=websockify'
```

## Chromium launch pattern

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

Why this matters:
- stable `user-data-dir` preserves state within the live browser
- fixed port `9222` gives Hermes a persistent CDP entrypoint
- `--no-sandbox` is needed when launching as root

## Hermes config that binds browser tools to the live session

```bash
hermes config set browser.cdp_url http://127.0.0.1:9222
hermes config set browser.engine chrome
hermes config set browser.command_timeout 60
```

## Required verification

1. CDP endpoint:

```bash
curl -fsS http://127.0.0.1:9222/json/version
```

Expected signal: response includes `webSocketDebuggerUrl`.

2. Browser tool path:
- run a real browser tool call against the target site
- confirm it succeeds from the configured CDP override path instead of the previously blocked default backend

3. Visible/UI parity:
- capture a screenshot from `:99`
- compare what the user sees in noVNC with what the browser tools report

## Good use case pattern

Use this pattern when:
- the site blocks the default browser tool path
- the user wants to watch login or navigation live
- the user wants future non-GUI browser operations to reuse the same browser state

## Common failure and fix

### Symptom
Chromium exits immediately and the CDP endpoint never opens.

### Likely cause
Running as root without `--no-sandbox`.

### Fix
Add `--no-sandbox` to the Chromium launch command.
