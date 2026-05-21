---
name: self-hosted-live-browser-cdp
description: Run a self-hosted visible Chromium session with a public noVNC watch URL and a stable CDP endpoint so Hermes browser tools and the user share the same browser state.
version: 1.0.0
author: <REDACTED_PUBLIC_BACKUP>
license: MIT
metadata:
  hermes:
    tags: [browser, cdp, novnc, xvfb, live-view, chromium, watchable-session]
    related_skills: [cloak-browser, captcha-aware-browsing, blocked-site-diagnostics]
---

# Self-Hosted Live Browser + CDP

## Overview

Use this skill when the user wants a **watchable browser session** that Hermes can also drive programmatically, especially when:

- the user wants a public live-view URL
- built-in browser automation is getting blocked or diverging from the visible browser
- the task needs the **same logged-in state** for GUI and non-GUI browser operations
- the user prefers self-hosted browser control over managed cloud live-preview sessions

The core pattern is:

1. start a local virtual desktop stack (`Xvfb` + window manager + `x11vnc` + `noVNC`)
2. expose it with a public tunnel
3. launch Chromium with a **stable remote debugging port**
4. persist `browser.cdp_url` so Hermes browser tools attach to that same live browser

This makes `browser_navigate`, `browser_snapshot`, `browser_click`, etc. operate against the same visible Chromium the user is watching.

## When to Use

- user asks for a visible/self-hosted browser session
- user wants a watch URL they can monitor live
- user wants future non-GUI browser operations to reuse the same browser session
- a target site behaves better in a local visible Chromium than in the default browser backend
- a login flow needs manual observation or occasional handoff

## Do Not Use For

- tasks that only need a quick hidden browser run with no shared state
- cases where Browser Use Cloud or another managed provider is explicitly preferred and funded
- tasks where no GUI/live view is useful

## Primary Workflow

1. **Start the desktop stack**
   - run `Xvfb` on a fixed display like `:99`
   - run a lightweight window manager such as `fluxbox`
   - run `x11vnc` on `5900`
   - run `novnc_proxy` on `6080`

2. **Expose the live view**
   - use a reverse tunnel such as `localhost.run`
   - share the `vnc_lite.html?...` URL with `autoconnect=1`
   - verify it returns HTTP 200 before claiming success

3. **Launch Chromium with a fixed CDP port**
   - use a stable `--user-data-dir`
   - use `--remote-debugging-address=127.0.0.1`
   - use `--remote-debugging-port=9222`
   - when running as root, include `--no-sandbox`
   - open the target site directly in this browser

4. **Persist Hermes browser defaults to this live browser**
   - set `browser.cdp_url` to `http://127.0.0.1:9222`
   - set `browser.engine` to `chrome`
   - increase `browser.command_timeout` if the site is slow
   - verify `curl http://127.0.0.1:9222/json/version` returns a `webSocketDebuggerUrl`

5. **Verify Hermes is really attached to the live browser**
   - run a browser tool call against the target page
   - confirm the browser tool reports `cdp_override` or otherwise clearly uses the configured CDP path
   - confirm the visible page matches the tool-observed page

## User Preferences This Skill Encodes

For this user, prefer:

- self-hosted watchable browser sessions
- reuse of the **same** live browser for GUI and non-GUI work
- humanized/CloakBrowser-style workflows when possible
- prompt-only handling of passwords and sensitive details

## Pitfalls

### 1. Starting a live browser without a CDP port
If Chromium is only visible but not launched with remote debugging, Hermes browser tools will still use a different backend. The user will think they are watching the same session, but they are not.

### 2. Forgetting `--no-sandbox` when running Chromium as root
A root-launched Chromium often fails immediately without `--no-sandbox`.

### 3. Tunnel looks up but noVNC is dead
Always verify the public `vnc_lite.html` URL with an HTTP request before sharing it.

### 4. Magnific / similar sites block the default backend but not the live CDP browser
If the default browser path is blocked, pivot to this pattern early instead of retrying the blocked backend repeatedly.

### 5. Saying non-GUI browser operations will reuse the live browser without verifying config
You must actually set `browser.cdp_url` and then test a real browser tool call.

## Verification Checklist

- [ ] visible desktop stack is listening on `5900` and `6080`
- [ ] public watch URL loads successfully
- [ ] Chromium is running with a stable `--remote-debugging-port`
- [ ] `curl .../json/version` returns a `webSocketDebuggerUrl`
- [ ] `browser.cdp_url` is persisted in Hermes config
- [ ] a real Hermes browser tool call succeeds against the target site
- [ ] user has the current watch URL

## Support Files

- `references/live-browser-stack.md` — concrete launch recipe, config keys, and troubleshooting notes from a successful session
