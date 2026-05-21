# Self-hosted noVNC + shared CDP browser pattern

## Goal
Run one Chromium instance that is both:
- visible to the user through noVNC
- addressable by Hermes browser tools through CDP

## Minimal recipe
1. Start Xvfb + Fluxbox + x11vnc + noVNC.
2. Launch Chromium with:
   - `--remote-debugging-address=127.0.0.1`
   - `--remote-debugging-port=9222`
   - `--no-sandbox` when running as root
3. Open the target site in that Chromium window.
4. Persist Hermes config:
   - `browser.cdp_url = http://127.0.0.1:9222`
   - `browser.engine = chrome`
   - `browser.command_timeout = 60`
5. Verify:
   - `curl http://127.0.0.1:9222/json/version`
   - successful Hermes `browser_navigate(...)`
   - tool output includes `cdp_override`

## Why this matters
Some targets behave differently between:
- the default Hermes browser path
- a visible local Chromium session

When the visible session works but the default path is blocked, routing Hermes through the live CDP browser preserves state and avoids splitting the workflow across two browsers.

## Session-learned pitfalls
- Root-launched Chromium fails without `--no-sandbox`.
- A working watch URL alone is insufficient; Hermes needs the CDP endpoint to share the same browser state.
- Browser Use Cloud billing/config is unrelated to this local live-browser pattern.
- If the tunnel URL expires, regenerate only the tunnel; the local CDP endpoint can stay unchanged.
