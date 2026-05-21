# Browser Use MCP and local live view with Hermes

This note captures a proven setup for two related workflows:

1. **Hermes ⇄ Browser Use Cloud via MCP**
2. **Self-hosted, user-viewable browser session from the same machine**

Use this when the user wants Hermes to either:
- control Browser Use Cloud from inside Hermes, or
- expose a live browser view URL the user can watch while Hermes drives a local browser.

## 1) Browser Use Cloud MCP wiring

Endpoint:

```text
https://api.browser-use.com/v3/mcp
```

Hermes config:

```yaml
mcp_servers:
  browser-use:
    url: https://api.browser-use.com/v3/mcp
    headers:
      x-browser-use-api-key: <REDACTED_PUBLIC_BACKUP>
    enabled: true
```

Secret placement:

```bash
# ~/.hermes/.env
MCP_BROWSER_USE_API_KEY=<REDACTED_PUBLIC_BACKUP>
```

Verification command:

```bash
hermes mcp test browser-use
```

Observed good result shape:
- successful HTTP connection
- Browser Use tools discovered, including:
  - `run_session`
  - `send_task`
  - `get_session`
  - `get_session_messages`
  - `stop_session`
  - `list_sessions`
  - `list_browser_profiles`

### Common gotchas

- **Fresh process required**: newly added MCP servers do not become callable mid-session. Restart the gateway or start a fresh Hermes process.
- **Balance errors are upstream**: if Browser Use returns *insufficient balance / need at least $1.00 / current balance $0.00*, treat that as a Browser Use Cloud account/project issue, not a Hermes MCP misconfiguration.
- **MCP package availability**: on some installs, the `mcp` Python package may need to be installed/upgraded in the Hermes runtime venv before HTTP MCP transport works reliably.

## 2) Self-hosted visible browser + public watch URL

This is useful when the user wants to **watch a live browser session** without depending on Browser Use Cloud live preview.

### Stack used successfully

Packages installed:

```bash
apt-get install -y x11vnc fluxbox novnc websockify xdotool
playwright install chromium
```

### Local display stack

Run an X virtual display, a window manager, VNC server, and noVNC proxy:

```bash
export DISPLAY=:99
Xvfb :99 -screen 0 1440x900x24 -ac +extension RANDR
fluxbox
x11vnc -display :99 -forever -shared -nopw -rfbport 5900
/usr/share/novnc/utils/novnc_proxy --vnc localhost:5900 --listen 6080
```

### Public tunnel

A working public URL was obtained with localhost.run:

```bash
ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=30 -R 80:localhost:6080 nokey@localhost.run
```

The session log prints a public HTTPS URL like:

```text
https://<random-subdomain>.lhr.life
```

A viewer-friendly endpoint is:

```text
https://<random-subdomain>.lhr.life/vnc_lite.html?autoconnect=1&resize=remote&path=websockify
```

### Browser launch

A visible browser was launched on the virtual display with Playwright's bundled Chromium:

```bash
DISPLAY=:99 playwright open https://magnific.com
```

### When built-in browser automation gets blocked

A useful fallback pattern is:
- if Hermes's built-in browser path gets a site-level 403 / security-filter block,
- but the user still wants a watchable live session,
- switch to the self-hosted Xvfb + noVNC path and drive a local Chromium window instead.

This preserves visibility for the user and avoids coupling the task to Browser Use Cloud billing or managed live-preview availability.

### Driving the visible session

`xdotool` worked well for keyboard/mouse control on the remote display, for example:

```bash
DISPLAY=:99 xdotool windowactivate --sync <window_id>
DISPLAY=:99 xdotool mousemove --window <window_id> X Y click 1
DISPLAY=:99 xdotool type --delay 20 'text here'
DISPLAY=:99 xdotool key Tab
DISPLAY=:99 xdotool key Return
```

Useful helpers:
- `xdotool search --onlyvisible --name 'Chrom'`
- `xdotool getwindowname <id>`
- `xdotool getwindowgeometry <id>`

### Login / verification-flow reliability notes

For email/password and 6-digit verification flows in a visible remote browser:
- confirm focus with a fresh screenshot before typing; `xdotool type` is fragile if the active field is uncertain
- if code-entry boxes are split across multiple inputs, bulk typing can drop or misplace the first digit; prefer a click into the first box and cautious entry
- after an incorrect-code response that clears the form, ask the user for a **fresh code** instead of repeatedly replaying the same one
- keep the public watch URL shared with the user so they can visually confirm what page/state they are seeing during login

### Verification / screenshots

A reliable way to inspect the X display is:

```bash
ffmpeg -y -f x11grab -video_size 1440x900 -i :99 -frames:v 1 /tmp/current.png
```

That image can then be visually checked to confirm page state before/after clicks.

## When to prefer this over Browser Use Cloud live preview

Prefer the self-hosted noVNC path when:
- Browser Use Cloud is blocked by billing/project issues
- the user specifically wants a **local visible browser** they can watch
- you only need a temporary shared watch link, not cloud session persistence

Prefer Browser Use Cloud live preview when:
- the account is funded and working
- the user wants managed sessions, cloud profiles, or Browser Use's own live preview/recording stack
