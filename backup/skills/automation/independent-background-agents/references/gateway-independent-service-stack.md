# Gateway-independent service stack pattern

Use this reference when the user wants background work and its supporting infrastructure to survive `hermes gateway restart`, Telegram gateway crashes, or live-chat model switches.

## Principle

Do not only make the agent job independent. Any long-lived supporting process it depends on should also be outside the gateway process tree:

- dashboard / monitoring UI
- public tunnel for monitoring
- visible browser desktop stack
- CDP Chromium instance
- local file/CORS preview server
- video/audio generation worker

If any of these is started by a gateway-bound terminal background process, a gateway restart can silently kill the run even if the agent prompt survives elsewhere.

## Startup checklist

1. Name every service explicitly with a stable `hermes-*` unit name.
2. Pin model/provider on each independent agent job, not in ambient chat state.
3. Put logs under a predictable path such as `/root/.hermes/independent_tasks/logs/NAME.log`.
4. Use `systemd-run --no-block --unit=...` for transient long-lived services.
5. For supervisor-like services, set `Restart=on-failure` when safe.
6. After starting, verify both systemd state and network listeners.

Example verification commands:

```bash
systemctl --no-pager --plain list-units 'hermes-*'
ss -ltnp | egrep ':9119|:4040|:9222|:6080|:5900|:8765' || true
```

## Restart / restore flow after gateway restart

1. List current units rather than relying on Hermes `process list`:

```bash
systemctl --no-pager --plain list-units 'hermes-*'
```

2. Restart only missing or failed units. Do not duplicate already-running browser/tunnel services unless the old ones are unhealthy.
3. Re-check public tunnel URL if the tunnel provider rotates hostnames.
4. Re-check CDP with `/json/version` before sending browser tools to the session.
5. Re-check the target job log before claiming progress resumed.

## Reporting to the user

When restoring a stack, report:

- unit names that are active,
- local ports/endpoints,
- public watch/dashboard URL if any,
- log paths for independent agent jobs,
- which model/provider each active agent job is pinned to.

Avoid stale one-off details in the skill itself. Put current session URLs and exact task IDs only in the live reply or session notes, not persistent skill text.
