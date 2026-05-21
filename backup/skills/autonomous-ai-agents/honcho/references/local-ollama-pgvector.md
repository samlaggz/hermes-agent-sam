# Local Honcho with Ollama + pgvector (CPU-friendly baseline)

Use this when the user wants Honcho self-hosted locally with local embeddings and a simple CPU-only setup.

## Durable lessons from a successful setup

1. Prefer local embeddings even on CPU-only machines.
   - A local embedding model is practical on CPU.
   - Keep retrieval local even if text-generation later moves to a remote API.

2. If using Ollama `nomic-embed-text`, verify embedding dimension before finalizing schema.
   - In this session the model returned dimension `768`.
   - Honcho/pgvector defaults may assume `1536`.
   - If dimensions differ, run Honcho's embedding configuration step so the DB schema and indexes match the actual model output.

3. Recommended baseline stack for local self-hosting:
   - PostgreSQL + pgvector
   - Ollama for local embeddings
   - Honcho API
   - Honcho deriver worker

4. For modest CPU-only hosts, use a lightweight local text model only if Honcho startup/features require one.
   - This can satisfy Honcho's generation requirements while keeping embeddings local.
   - If latency or CPU load becomes a problem, keep embeddings local and move only text-generation to a remote API.

5. Persistence checklist after setup:
   - Run DB migrations
   - Reconfigure embeddings if model dimension differs from schema defaults
   - Put API and deriver under systemd
   - Verify both services are active
   - Verify the health endpoint returns OK
   - Verify Hermes can read/write through the Honcho provider

## Verification targets

- Honcho health endpoint returns `{\"status\":\"ok\"}`
- Both long-running services are active after restart
- Hermes memory provider status shows `honcho`
- A simple cross-session recall test succeeds

## Pitfall to remember

The durable lesson is not any one path or binary name; it is this: service unit `ExecStart` targets must point at stable, actually-present executables, and startup should always be verified with service status, logs, and the Honcho health endpoint.
