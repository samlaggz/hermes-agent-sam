# Memory backends and local-hosting notes

Use this note when the user asks how Hermes memory, vector storage, or self-hosted Honcho fit together.

## Persistence layers in Hermes

Keep the three layers distinct:

- `~/.hermes/sessions/` — full session transcripts / history
- Built-in memory — compact durable facts about the user and environment
- `~/.hermes/skills/` — reusable workflows and procedures

Important invariants:

- Built-in memory is always active unless reset.
- Only one external memory provider can be active at a time.
- External/vector memory improves retrieval; it is not a replacement for full session storage.

## Vector storage: storage-space caveat

Do not pitch vector memory as a storage-saving mechanism.

Reason:
- Storing raw text plus embeddings usually increases total storage.
- The value of vector memory is semantic recall quality, not zero-cost archival.

Recommended framing:
- Sessions = full archive
- Memory backend = retrieval layer
- Built-in memory = compact durable facts
- Skills = reusable know-how

## Honcho: model ownership and self-hosting

When Hermes uses Honcho, Hermes is the client and Honcho is the memory server.

Hermes-side config for Honcho mostly controls:
- `baseUrl`
- `apiKey`
- recall / cadence / session strategy / observation behavior

Do not claim Hermes directly configures Honcho's internal embedding or reasoning models the way Hindsight local mode does. Those choices live on the Honcho deployment side.

## Honcho local/self-hosted guidance

Self-hosted Honcho requires:
- Honcho server
- PostgreSQL with pgvector
- LLM provider config (server fails to start without one)

The Honcho docs say:
- Built-in defaults use `openai / gpt-5.4-mini` for text-generation features.
- Built-in defaults use `openai / text-embedding-3-small` for embeddings.
- Any OpenAI-compatible endpoint works too, including Ollama and vLLM.

## Practical hardware guidance for a CPU-only box

For a machine around:
- 8 vCPU
- ~31 GiB RAM
- no GPU

Recommended deployment shape:
- Honcho API: local
- PostgreSQL + pgvector: local
- Embedding model: local via an OpenAI-compatible endpoint (for example Ollama)
- Text-generation features (deriver / summary / dialectic / dream): remote API

Why:
- Local embeddings are realistic on CPU-only hardware.
- Fully local high-quality reasoning for all Honcho text features is technically possible only in a limited/testing sense and is usually too slow on this class of machine.
- The best balance is local memory + local embeddings + remote text LLMs.

## Embedding config notes from Honcho docs

Honcho embedding config is separate from text-generation config.

Key env vars shown in Honcho docs:
- `EMBEDDING_VECTOR_DIMENSIONS`
- `EMBEDDING_MODEL_CONFIG__TRANSPORT`
- `EMBEDDING_MODEL_CONFIG__MODEL`
- `EMBEDDING_MODEL_CONFIG__OVERRIDES__BASE_URL`

Example pattern for local embeddings:
- `EMBEDDING_MODEL_CONFIG__TRANSPORT=openai`
- `EMBEDDING_MODEL_CONFIG__MODEL=<local embedding model>`
- `EMBEDDING_MODEL_CONFIG__OVERRIDES__BASE_URL=http://localhost:11434/v1`

Important caveat:
- Embedding dimension is deployment-pinned.
- Changing embedding dimension or model later is a destroy-and-rebuild / new-deployment migration, not a casual in-place toggle.
