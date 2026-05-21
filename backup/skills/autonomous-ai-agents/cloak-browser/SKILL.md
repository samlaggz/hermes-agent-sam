---
name: cloak-browser
description: Managing CloakBrowser/ghost integration with Python and Playwright.
---

# CloakBrowser Integration

Specialized workflows for managing and deploying the `Clots/CloakBrowser` (ghost) engine within a Python/Playwright environment. 

## Workflow: Setup & Link
1. **Link established:** Ensure the source directory (`~/ghost`) is symlinked to the target Python site-packages directory in the active venv.
2. **Verification:** Verify `from ghost import launch` works without error.

## Workflow: Stealth Interaction (The "Ghost" Standard)
1. **Humanize Flag:** Use `humanize=True` when interacting with sensitive sites to leverage built-in behavioral emulation.
2. **Validation:** Check if the browser instance correctly resolves content in headless mode.

## Workflow: Visible Watchable Session
When the user wants to watch the browser live, or when a target behaves differently in Hermes browser tools vs a local visible browser:
1. Start a visible desktop stack (Xvfb + WM + x11vnc + noVNC/websockify).
2. Expose the noVNC endpoint with a watchable URL.
3. Launch CloakBrowser with `headless=False` and `humanize=True` inside that display.
4. Verify the public watch URL before sharing it.
5. Keep the process alive so the user can observe or take over.

Reference: `references/visible-watch-session.md`

## Pitfalls & Troubleshooting
- **Link Mismatch:** If `ghost` is not found, verify the current Python environment matches the target directory of the symlink.
- **Venv Mismatch:** On this setup, `ghost` imported from `/root/cloak_venv/bin/python`; system `python3` did not have the package.
- **Empty Titles:** In headless mode on remote servers, ensure the engine has enough time to resolve the DOM before reading titles.
- **Watchability:** For user-observable sessions, do not use headless mode; launch into a real display and keep the browser open.
