# Visible Browser + Public Watch URL

Reusable pattern for login/verification tasks where the user wants a self-hosted browser they can watch live.

## Minimal stack
- `Xvfb` for a headless X display (example: `:99`)
- `fluxbox` or another lightweight window manager
- `x11vnc` exposing the X display over VNC (example: port `5900`)
- `noVNC` / `websockify` exposing VNC in the browser (example: port `6080`)
- a public tunnel for the noVNC port (reverse SSH via `localhost.run` worked well in this session)

## Reliable execution order
1. Start `Xvfb`.
2. Start the window manager in the same display.
3. Start `x11vnc` against that display.
4. Start `noVNC` / `websockify` pointing at the VNC port.
5. Verify listeners locally.
6. Expose the noVNC port publicly.
7. Confirm the public URL returns HTTP 200.
8. Launch the browser with the same `DISPLAY` so the user sees every action.

## Verification checklist
- Confirm local listeners on the expected ports before tunneling.
- Confirm the public watch URL loads successfully before sharing it.
- Keep the browser window ID handy if using X11 automation tools like `xdotool`.
- For state inspection, a quick screenshot via `ffmpeg -f x11grab ... -frames:v 1` is a reliable check.

## OTP / verification-screen pitfall
Multi-field code-entry UIs can mis-handle focus under automation and silently drop the first digit.

Safer pattern:
- click/focus the first box explicitly
- type more slowly or in smaller chunks
- capture a screenshot after entry
- if the code fails, do not assume the code itself was wrong until the filled UI is verified
- when a code was re-sent, prefer the newest code rather than retrying the old one blindly

## Asset-creation follow-through
If the same session becomes a creative production task, do not stop at exploration:
- inspect the creation app's available video/audio/voice/stock tools first
- gather legal source assets
- render the deliverable file
- save a script and asset/source manifest with the final output
