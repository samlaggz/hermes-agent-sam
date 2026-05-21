# Honcho pre-fallback compression for Hermes

Use this when the user wants model failover to compact context first, especially with OpenRouter free-model fallback chains.

## Durable lessons from this session

1. Honcho is an exclusive memory-provider plugin.
   - Do not try `hermes plugins enable honcho`.
   - Correct activation path:
     - `hermes config set memory.provider honcho`
     - verify with `hermes memory status`
     - inspect with `hermes honcho status`

2. A local Honcho deployment can be considered active without `HONCHO_API_KEY` when `honcho.json` points at a reachable `baseUrl`.
   - Example status looked healthy with:
     - `baseUrl: http://127.0.0.1:8000`
     - `memory.provider: honcho`
     - `hermes honcho status` returning `OK`

3. Hermes fallback chains are built-in, but “compress with Honcho before switching models” is not just a config toggle in this install.
   - Built-in fallback behavior already switches on rate limit / overload / connection errors.
   - To force pre-fallback compression, patch source so fallback activation can:
     - detect active Honcho provider
     - call `_compress_context(...)` before swapping model/provider
     - propagate compressed message state back into the main conversation loop

## Patch points that worked

Files changed:
- `agent/chat_completion_helpers.py`
- `agent/conversation_loop.py`
- `run_agent.py`

Implementation pattern:

### 1. Extend fallback activation signature
Allow `_try_activate_fallback(...)` / `try_activate_fallback(...)` to accept:
- `messages`
- `system_message`
- `active_system_prompt`
- `task_id`
- `approx_tokens`

### 2. Add a best-effort pre-fallback compression helper
In `agent/chat_completion_helpers.py`, add a helper that:
- checks `agent._memory_manager._providers`
- proceeds only if one provider has `name == "honcho"`
- estimates tokens with `estimate_request_tokens_rough(...)` if needed
- calls:
  - `agent._compress_context(messages, system_message, approx_tokens=..., task_id=...)`
- stores the updated transcript on `agent._session_messages`
- sets a flag such as `agent._fallback_compressed_messages_ready = True`
- never blocks fallback if compression fails

### 3. Sync compressed state back into the loop
In `agent/conversation_loop.py`, after each successful fallback activation call:
- replace local `messages` with `agent._session_messages` when the flag is set
- refresh `active_system_prompt` from `agent._cached_system_prompt`
- clear the flag

### 4. Update every fallback call site, not just one
Fallback happens in several branches:
- early empty / malformed response path
- invalid-response retry exhaustion
- rate-limit fallback path
- non-retryable client-error path
- max-retries-exhausted path
- empty-content terminal path

Patch all call sites that invoke `agent._try_activate_fallback(...)`, or behavior will be inconsistent.

### 5. Preserve extracted helper dependencies after refactors
During verification, Hermes crashed with:
- `NameError: name '_pool_may_recover_from_rate_limit' is not defined`

Fix pattern:
- if `conversation_loop.py` references a helper that historically lived on `run_agent.py`, add a small forwarder in `conversation_loop.py` that delegates via `_ra()`.
- Then rerun a real CLI smoke test.

## Verification checklist

1. Syntax check patched files:
```bash
python3 -m py_compile /usr/local/lib/hermes-agent/agent/chat_completion_helpers.py \
  /usr/local/lib/hermes-agent/agent/conversation_loop.py \
  /usr/local/lib/hermes-agent/run_agent.py
```

2. Verify Honcho activation:
```bash
hermes memory status
hermes honcho status
```

3. Verify fallback chain:
```bash
hermes fallback list
```

4. Run a real chat smoke test:
```bash
hermes chat -Q -q 'Reply with exactly OK'
```

## Pitfalls

- `hermes plugins list` may show Honcho as installed while `hermes plugins enable honcho` still fails. That is expected for exclusive memory-provider plugins.
- Do not save “Honcho is broken” or “plugin enable failed” as a general lesson. The durable lesson is the correct activation path.
- If OpenRouter free models are flaky, preserve the strongest-first fallback ordering but expect some top models to 429 intermittently.
- Reinstalling/updating Hermes may overwrite source patches; mention this explicitly to the user.
