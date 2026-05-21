# Browser Use Cloud MCP with Hermes

Use this when the user wants Browser Use Cloud available as Hermes MCP tools rather than via the built-in browser stack.

## Known-good config

```yaml
mcp_servers:
  browser-use:
    url: "https://api.browser-use.com/v3/mcp"
    headers:
      x-browser-use-api-key: <REDACTED_PUBLIC_BACKUP>
    enabled: true
```

## Secret placement

Store the secret in `~/.hermes/.env`:

```bash
MCP_BROWSER_USE_API_KEY=<REDACTED_PUBLIC_BACKUP>
```

Hermes MCP config supports `${VAR}` interpolation from the runtime environment / Hermes `.env`.

## Verification flow

1. Ensure the Hermes runtime environment has `mcp` installed/upgraded.
2. Add the server config.
3. Run:

```bash
hermes mcp test browser-use
```

Expected tool family includes:
- `run_session`
- `get_session`
- `send_task`
- `get_session_messages`
- `stop_session`
- `list_sessions`
- `list_browser_profiles`

4. Restart Hermes (`/restart`, `/reset`, or relaunch CLI) before expecting the tools to appear in-chat.

## Important distinction

A successful MCP connection does **not** guarantee Browser Use Cloud can actually launch sessions. In this session the server connected and advertised tools, but later `run_session` failed because the Browser Use account had insufficient balance. Treat these as separate checks:

- MCP connectivity/auth works
- Browser Use Cloud project billing/account state allows session execution

## Symptom pattern

- `hermes mcp test browser-use` succeeds
- actual Browser Use session creation fails with an insufficient-balance error

Interpretation: Hermes-side MCP setup is correct; the remaining blocker is Browser Use Cloud account state, not Hermes MCP wiring.
