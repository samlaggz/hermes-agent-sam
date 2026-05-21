# Honcho local embeddings on a CPU-only server

Use this when the user wants Honcho self-hosted on a modest Linux box and only truly needs local text embeddings.

## Durable lesson

Honcho will not start without an LLM provider configured for its text-generation features, even if the user's real goal is only local embeddings.

So the minimal workable shape is:
- PostgreSQL + pgvector locally
- Honcho API locally
- Honcho deriver locally
- Local embedding endpoint via an OpenAI-compatible server
- A text-generation model configured for Deriver / Summary / Dialectic so Honcho can boot

## Good CPU-only pattern

For a machine around 8 vCPU / 31 GiB RAM / no GPU:
- Local embeddings: yes, realistic
- Fully local high-quality reasoning for all Honcho text features: possible but slow
- Pragmatic local-only bootstrap: small local text model + local embedding model

Recommended bootstrap stack:
- PostgreSQL 17 + pgvector
- Ollama
- `nomic-embed-text` for embeddings
- `qwen3:8b` as the minimum local text model so Honcho can start
- `DREAM_ENABLED=false` on CPU-only boxes unless the user explicitly wants heavier background consolidation

## Debian 13 bootstrap notes

Packages used successfully:
```bash
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y \
  postgresql postgresql-contrib postgresql-17-pgvector curl
```

Enable pgvector:
```bash
sudo -u postgres psql -v ON_ERROR_STOP=1 -d postgres \
  -c "ALTER USER postgres PASSWORD 'postgres';" \
  -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

Install Ollama and pull models:
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull nomic-embed-text
ollama pull qwen3:8b
```

Verify embedding dimension before configuring Honcho schema:
```bash
curl -s http://127.0.0.1:11434/api/embeddings \
  -d '{"model":"nomic-embed-text","prompt":"hello world"}' \
  -H 'Content-Type: application/json'
```
Expected dimension observed in-session: `768`.

## Honcho env shape

Minimal local `.env` pattern:
```dotenv
DB_CONNECTION_URI=postgresql+psycopg://postgres:postgres@localhost:5432/postgres
AUTH_USE_AUTH=<REDACTED_PUBLIC_BACKUP>
CACHE_ENABLED=false
LLM_OPENAI_API_KEY=<REDACTED_PUBLIC_BACKUP>

EMBEDDING_VECTOR_DIMENSIONS=768
EMBEDDING_MODEL_CONFIG__TRANSPORT=openai
EMBEDDING_MODEL_CONFIG__MODEL=nomic-embed-text
EMBEDDING_MODEL_CONFIG__OVERRIDES__BASE_URL=http://127.0.0.1:11434/v1
EMBEDDING_MODEL_CONFIG__DIMENSIONS_MODE=never

DERIVER_MODEL_CONFIG__TRANSPORT=openai
DERIVER_MODEL_CONFIG__MODEL=qwen3:8b
DERIVER_MODEL_CONFIG__OVERRIDES__BASE_URL=http://127.0.0.1:11434/v1

SUMMARY_MODEL_CONFIG__TRANSPORT=openai
SUMMARY_MODEL_CONFIG__MODEL=qwen3:8b
SUMMARY_MODEL_CONFIG__OVERRIDES__BASE_URL=http://127.0.0.1:11434/v1

DIALECTIC_LEVELS__minimal__MODEL_CONFIG__TRANSPORT=openai
DIALECTIC_LEVELS__minimal__MODEL_CONFIG__MODEL=qwen3:8b
DIALECTIC_LEVELS__minimal__MODEL_CONFIG__OVERRIDES__BASE_URL=http://127.0.0.1:11434/v1

DREAM_ENABLED=false
```

## Critical pitfall

When switching Honcho from the default `text-embedding-3-small` assumption to `nomic-embed-text`, the pgvector columns must be changed from 1536 dims to 768 dims before serving traffic.

Use:
```bash
uv run alembic upgrade head
uv run python scripts/configure_embeddings.py --yes
```

This is the important reusable lesson: match `EMBEDDING_VECTOR_DIMENSIONS` to the actual embedding model output before first real writes.

## Hermes wiring

Hermes-side config can stay simple:
- set `memory.provider` to `honcho`
- point `~/.hermes/honcho.json` at the local Honcho `baseUrl`
- keep `recallMode` as `hybrid` unless the user wants tool-only behavior

Example:
```json
{
  "baseUrl": "http://127.0.0.1:8000",
  "workspace": "hermes",
  "hosts": {
    "hermes": {
      "enabled": true,
      "aiPeer": "hermes",
      "recallMode": "hybrid",
      "sessionStrategy": "per-directory",
      "writeFrequency": "async",
      "dialecticReasoningLevel": "minimal"
    }
  }
}
```

## Verification

```bash
curl http://127.0.0.1:8000/health
hermes memory status
hermes honcho status
hermes chat -q "Remember that my favorite fruit is mango."
hermes chat -q "What do you know about my preferences?"
```

If the second chat recalls the fact in a fresh session, the end-to-end path is working.
