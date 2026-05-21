# OpenAI-managed models for self-hosted Honcho

Use this when the user wants to keep Honcho self-hosted but replace local CPU-bound models with managed OpenAI models for better speed/efficiency.

## Durable lesson

Do not conflate the Hermes chat provider (for example Codex/OpenAI auth used by Hermes itself) with Honcho's internal model configuration. Honcho embeddings and Honcho text-generation tasks are configured separately in Honcho's own `.env`.

## What counts as Honcho "text tasks"

These are the non-embedding model roles inside Honcho:
- `DERIVER_MODEL_CONFIG__...` — background extraction/consolidation
- `SUMMARY_MODEL_CONFIG__...` — session summaries
- `DIALECTIC_LEVELS__...__MODEL_CONFIG__...` — synthesized memory reasoning

## Recommended managed replacement for a local CPU-only qwen3:8b setup

Best overall balance for this class of deployment:
- Embeddings: `text-embedding-3-small`
- Text tasks: `gpt-4.1-mini`

Why:
- `text-embedding-3-small` is usually the best quality/speed/cost tradeoff for memory retrieval.
- `gpt-4.1-mini` is a strong replacement for local `qwen3:8b` when the user wants better latency and lower local CPU load without paying flagship-model prices.

## When to choose other models

Use `text-embedding-3-large` only when retrieval quality matters more than cost/latency.

Use a larger chat model than `gpt-4.1-mini` only when the user explicitly wants maximum reasoning quality for Honcho summaries/dialectic and accepts higher cost.

## Config shape

Typical `.env` pattern:

```dotenv
LLM_OPENAI_API_KEY=<REDACTED_PUBLIC_BACKUP>

EMBEDDING_MODEL_CONFIG__TRANSPORT=openai
EMBEDDING_MODEL_CONFIG__MODEL=text-embedding-3-small

DERIVER_MODEL_CONFIG__TRANSPORT=openai
DERIVER_MODEL_CONFIG__MODEL=gpt-4.1-mini

SUMMARY_MODEL_CONFIG__TRANSPORT=openai
SUMMARY_MODEL_CONFIG__MODEL=gpt-4.1-mini

DIALECTIC_LEVELS__minimal__MODEL_CONFIG__TRANSPORT=openai
DIALECTIC_LEVELS__minimal__MODEL_CONFIG__MODEL=gpt-4.1-mini
DIALECTIC_LEVELS__low__MODEL_CONFIG__TRANSPORT=openai
DIALECTIC_LEVELS__low__MODEL_CONFIG__MODEL=gpt-4.1-mini
DIALECTIC_LEVELS__medium__MODEL_CONFIG__TRANSPORT=openai
DIALECTIC_LEVELS__medium__MODEL_CONFIG__MODEL=gpt-4.1-mini
DIALECTIC_LEVELS__high__MODEL_CONFIG__TRANSPORT=openai
DIALECTIC_LEVELS__high__MODEL_CONFIG__MODEL=gpt-4.1-mini
DIALECTIC_LEVELS__max__MODEL_CONFIG__TRANSPORT=openai
DIALECTIC_LEVELS__max__MODEL_CONFIG__MODEL=gpt-4.1-mini
```

## Critical migration warning

If replacing a local embedding model such as `nomic-embed-text` with an OpenAI embedding model, verify and align `EMBEDDING_VECTOR_DIMENSIONS` with the new model before serving traffic. If dimensions change, re-run the Honcho embedding/schema configuration workflow before restart.

Important populated-table pitfall:
- Honcho's `scripts/configure_embeddings.py --yes` refuses to alter populated embedding tables.
- If the current deployment already contains embeddings, a naive switch from 768-dim local embeddings to a 1536-dim OpenAI default will be blocked.

Practical workaround when using `text-embedding-3-small`:
- keep the existing schema dimension
- set `EMBEDDING_VECTOR_DIMENSIONS` to the existing dimension
- set `EMBEDDING_MODEL_CONFIG__DIMENSIONS_MODE=always`
- let OpenAI return embeddings at that explicit size

This avoids destructive migration and keeps the service online, but there is an accuracy tradeoff:
- existing stored vectors from the old embedding model remain in the index
- new vectors come from a different model family
- retrieval quality may be mixed until old embeddings are rebuilt or cleared

So there are two valid migration paths:
1. Fast non-destructive cutover: keep the old dimension and start writing new OpenAI embeddings immediately.
2. Clean rebuild: clear/recreate embeddings, change schema dimension to the new default, and re-embed into a uniform vector space.

The reusable lesson is: model swap decisions for Honcho should be made per role:
- embeddings for retrieval economics
- text tasks for summary/reasoning latency and quality
rather than assuming one provider choice automatically applies to both.
