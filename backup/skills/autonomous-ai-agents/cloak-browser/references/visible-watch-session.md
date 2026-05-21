# Visible self-hosted watch session with CloakBrowser

Use this when the user wants a browser session they can watch live, especially after anti-bot/security differences between built-in browser tools and a local visible browser.

## When this applies
- User asks for a live watch URL / visible browser session
- Target behaves differently in the built-in browser tools than in a local desktop browser
- You need the user to watch or manually take over

## Proven pattern
1. Start a virtual desktop on `:99` with Xvfb.
2. Start a lightweight WM (e.g. Fluxbox).
3. Start `x11vnc` on port `5900`.
4. Start noVNC/websockify on port `6080`.
5. Expose `6080` with a temporary public tunnel (for example `ssh -R 80:localhost:6080 nokey@localhost.run`).
6. Launch CloakBrowser inside that display using the CloakBrowser venv and `humanize=True`.
7. Keep the browser process alive so the user can watch / take over.

## Minimal launch pattern
```bash
export DISPLAY=:99
/root/cloak_venv/bin/python your_script.py
```

```python
import time
from ghost import launch

browser = launch(headless=False, humanize=True)
page = browser.new_page()
page.goto('https://www.example.com', wait_until='domcontentloaded', timeout=120000)
while True:
    time.sleep(60)
```

## Notes
- The system Python may not have `ghost`; the CloakBrowser venv did.
- For watchable sessions, `headless=False` is required.
- `humanize=True` matches the user's preferred default for sensitive sites.
- Verify the watch URL itself (for example with `curl -I`) before handing it to the user.
- If the target site is blocked in Hermes browser tools but accessible in the visible session, continue only with legitimate browsing/diagnostics; do not turn the workflow into a bypass recipe.
