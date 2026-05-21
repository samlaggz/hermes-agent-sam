# LM Studio local models with Hermes

Use this when the user has LM Studio running a local OpenAI-compatible server and wants Hermes CLI to use it.

## Fast path

If Hermes runs on the same machine as LM Studio:

- Base URL: `http://127.0.0.1:1234/v1`
- API key: any non-empty placeholder usually works, e.g. `lm-studio`
- Provider in Hermes: `openai` or `Custom Endpoint` via `hermes model`
- Model name: must exactly match the model ID exposed by LM Studio

## Recommended setup

Interactive:

```bash
hermes model
# choose: Custom Endpoint
# set base URL to http://127.0.0.1:1234/v1
# set API key to lm-studio
# set model to the exact LM Studio model name
```

Manual config:

```bash
hermes config set model.provider openai
hermes config set model.base_url http://127.0.0.1:1234/v1
hermes config set model.default <exact-lm-studio-model-name>
```

Then add the API key placeholder to Hermes env:

```bash
# path: hermes config env-path
OPENAI_API_KEY=<REDACTED_PUBLIC_BACKUP>
```

Restart Hermes after config/env changes.

## Verification

```bash
hermes chat --provider openai -m <exact-lm-studio-model-name> -q "Reply with exactly: local model works"
```

Expected response:

```text
local model works
```

## Common pitfalls

- `127.0.0.1` only works if Hermes and LM Studio are on the same machine.
  - If Hermes is elsewhere, expose LM Studio on a LAN IP or tunnel it.
- Wrong model name is the most common failure. Copy the exact model ID from LM Studio.
- Hermes is happiest with models that support tool use well and have large context.
- Hermes needs at least about 64K context for practical agent workflows. Local models below that are a poor fit.
- If the endpoint responds but the agent behaves badly, the model may be too weak for multi-step tool calling even if the HTTP setup is correct.

## Remote Hermes + local LM Studio via reverse SSH tunnel

This pattern matters when Hermes runs on a server but LM Studio runs on the user's local machine.

Typical shape:
- Hermes config points to `http://127.0.0.1:1234/v1`
- but that `127.0.0.1` is on the Hermes server, not the user's laptop
- so it only works when a reverse SSH tunnel is currently active from the local machine to the server

Practical rule:
- Do **not** switch Hermes to the LM Studio model just because logs show it worked previously.
- First verify that the tunnel endpoint is live **right now** from the Hermes host.

Recommended verification before changing config:

```bash
python3 - <<'PY'
import urllib.request
for url in ['http://127.0.0.1:1234/v1/models', 'http://localhost:1234/v1/models']:
    try:
        with urllib.request.urlopen(url, timeout=8) as r:
            print(url, r.status)
            print(r.read().decode('utf-8', 'replace')[:500])
    except Exception as e:
        print(url, repr(e))
PY

ss -ltnp | grep 1234 || true
ps -ef | grep -E 'ssh|autossh' | grep -v grep
```

Interpretation:
- If `/v1/models` responds and port 1234 is listening, it's safe to switch Hermes config.
- If it returns connection refused and nothing is listening on 1234, the reverse tunnel is down; do **not** repoint Hermes yet.
- Historical Hermes logs can confirm the old setup (`provider=custom`, `base_url=http://127.0.0.1:1234/v1`, model name), but logs are not proof that the tunnel is still live.

Only after a live check passes should you set:

```bash
hermes config set model.provider openai
hermes config set model.base_url http://127.0.0.1:1234/v1
hermes config set model.default <exact-lm-studio-model-name>
```

Also remember:
- config changes require a fresh Hermes session / relaunch to take effect cleanly
- keep the current hosted model in place if the tunnel is down, so you don't strand the agent on an unreachable endpoint

## When to recommend against it

If the user's local model is weak at tool use or has a small context window, suggest:
- keeping a hosted model as the main Hermes model, or
- using the local LM Studio model only for experimentation or narrow tasks.
