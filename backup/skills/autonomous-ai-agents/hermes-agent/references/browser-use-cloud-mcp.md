# Browser Use Cloud MCP with Hermes

Use this when the user wants Hermes itself to call Browser Use Cloud sessions through MCP.

## Why this matters

Browser Use exposes an MCP endpoint at:

`https://api.browser-use.com/v3/mcp`

Hermes can connect to it as a native HTTP MCP server and then surface Browser Use tools directly in chat.

## Important gotcha: header auth shape

The Browser Use MCP endpoint expects this header:

- `x-browser-use-api-key: <bu_... key>`

Do **not** rely on `hermes mcp add ... --auth header` for this integration if you need it fully working immediately, because Hermes's generic HTTP-header auth path stores:

- `Authorization: Bearer ${MCP_<NAME>_API_KEY}`

That is correct for many MCP servers, but not for Browser Use MCP.

For Browser Use, prefer a manual config entry in `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  browser-use:
    url: https://api.browser-use.com/v3/mcp
    headers:
      x-browser-use-api-key: <REDACTED_PUBLIC_BACKUP>
    enabled: true
```

And store the key in `~/.hermes/.env`:

```bash
MCP_BROWSER_USE_API_KEY=<REDACTED_PUBLIC_BACKUP>
```

## Verification

After saving config and env:

```bash
hermes mcp test browser-use
hermes mcp list
```

A successful test should discover Browser Use tools such as:
- `run_session`
- `send_task`
- `get_session`
- `get_session_messages`
- `stop_session`
- `list_sessions`
- `list_browser_profiles`

## Restart / reload semantics

New MCP servers do not become available mid-conversation.

Use one of:
- Telegram / gateway: `/restart`
- CLI: restart Hermes
- Fresh session after reload when applicable

If the user says "it is configured but the tools still are not available", first check whether the process/session was restarted after editing `mcp_servers`.

## Browser Use Cloud billing pitfall

Even when MCP auth is correct, Browser Use Cloud may reject `run_session` with an insufficient-balance error.

Typical API error:
- need at least `$1.00`
- current balance `$0.00`

If that happens, the integration itself may still be healthy. Distinguish clearly between:
- **MCP connection success**
- **Browser Use Cloud account/project billing readiness**

In that case:
1. report that the MCP server is configured correctly if `hermes mcp test browser-use` succeeds
2. explain that session launch is blocked by Browser Use account billing/project state
3. point the user to Browser Use billing/project settings rather than redoing Hermes config
