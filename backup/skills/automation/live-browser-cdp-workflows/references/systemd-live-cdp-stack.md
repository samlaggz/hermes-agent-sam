# Systemd-backed live browser CDP stack

Use this when the visible browser must stay alive across Telegram gateway restarts or live-chat model changes.

## Durable components

Run each component outside the gateway process tree, normally as named systemd units:

- `hermes-liveview-stack` — Xvfb, window manager, x11vnc, noVNC/websockify
- `hermes-live-browser` — Chromium with a fixed `--remote-debugging-port`, usually `9222`
- `hermes-ngrok-dashboard` or another tunnel unit when a public URL is required

The exact tunnel hostname is volatile; do not store it in skill text.

## Chromium launch requirements

For root/server execution, Chromium generally needs:

```bash
chromium \
  --no-sandbox \
  --remote-debugging-address=127.0.0.1 \
  --remote-debugging-port=9222 \
  --user-data-dir=/root/.cache/hermes-live-browser \
  --window-size=1440,900
```

Use the visible display environment (`DISPLAY=:99` or equivalent) so the same browser is both watchable through noVNC and controllable over CDP.

## Health checks

Before using browser tools or telling the user the session is restored:

```bash
systemctl --no-pager --plain list-units 'hermes-live*' 'hermes-ngrok*'
curl -fsS http://127.0.0.1:9222/json/version
ss -ltnp | egrep ':9222|:6080|:5900' || true
```

If the live viewer is public, verify the URL loads. If a tunnel restarted, surface the new URL clearly.

## Common pitfall

Starting noVNC or Chromium from a gateway-bound background process makes the session disappear on `hermes gateway restart`. For durable tasks, prefer systemd units and reserve Hermes `process` for short-lived or disposable work.
