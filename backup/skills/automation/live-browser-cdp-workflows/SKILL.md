---
name: live-browser-cdp-workflows
description: Run a self-hosted visible browser with a stable CDP endpoint, then reuse that same browser for both watchable GUI flows and non-GUI Hermes browser operations.
---

# Live Browser CDP Workflows

Use this skill when the user wants a **watchable self-hosted browser session** and also wants Hermes browser tools to operate against that **same live browser** instead of spawning a separate hidden session.

## When to use
- User wants a public watch URL for a browser session.
- A target site behaves better in a visible local Chromium session than in the default browser path.
- The user wants GUI and non-GUI browser work to share one browser state.
- The user wants login/manual handoff in a visible session, then later automated navigation against the same browser.

## Core pattern
1. Start a self-hosted browser desktop stack.
   - Xvfb / window manager / x11vnc / noVNC.
   - Expose it with a public tunnel when needed.
   - If the session must survive gateway restarts, run the stack as named systemd units rather than Hermes gateway-bound background processes.
2. Launch Chromium with a **stable remote debugging port**.
   - Prefer a fixed local CDP endpoint like `http://127.0.0.1:9222`.
   - For durable live work, launch Chromium itself as an independent service too, not as a child of the chat/gateway process.
3. Persist Hermes browser config to reuse that browser.
   - Set `browser.cdp_url` to the local CDP endpoint.
   - Set `browser.engine` to `chrome`.
   - Increase `browser.command_timeout` when the site is heavy.
4. Verify the CDP endpoint before trusting the setup.
   - Confirm `/json/version` returns a `webSocketDebuggerUrl`.
5. Use Hermes browser tools normally.
   - If configured correctly, tool output should show `cdp_override` and browser tasks will run in the same live Chromium session.

## User-specific workflow preference
For this user, prefer:
- self-hosted watchable sessions over cloud live-preview when possible
- one shared browser for both live watching and non-GUI browser tool operations
- humanized CloakBrowser-style workflow when possible, but stable shared CDP reuse is the first priority

## Recommended persisted settings
Store these in Hermes config when the user wants this behavior as the default:

```yaml
browser:
  cdp_url: http://127.0.0.1:9222
  engine: chrome
  command_timeout: 60
```

## Verification checklist
- Live viewer URL opens successfully.
- Chromium is visibly open to the intended site.
- `curl http://127.0.0.1:9222/json/version` succeeds.
- Hermes browser navigation succeeds against the target site.
- Browser tool output indicates CDP override routing.

## Pitfalls
- If Chromium runs as root, add `--no-sandbox` or the browser will fail to start.
- A visible browser is not enough; without a stable remote-debugging port Hermes may still spawn a different session.
- When starting a full self-hosted stack (Xvfb + x11vnc + websockify/noVNC + Chromium), use `terminal(background=true)` for the long-lived supervisor process, then run CDP/noVNC health checks in separate foreground calls. Do not try to start several daemons with shell-level `&` in a foreground terminal call; Hermes rejects foreground commands that background child processes.
- If the tunnel dies, regenerate the watch URL, but keep the CDP endpoint stable.
- If the site allows the live Chromium path but blocks the default browser path, switch Hermes to the live CDP endpoint rather than retrying the blocked path.
- Do not assume Browser Use Cloud settings affect the local live browser workflow; they are separate backends.

## Support files
- `references/self-hosted-novnc-cdp.md` — concise setup notes and verification pattern for the shared live-browser/CDP workflow.
- `references/systemd-live-cdp-stack.md` — durable systemd-backed pattern for live browser/noVNC/CDP stacks that must survive gateway restarts.
