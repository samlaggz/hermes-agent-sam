# OpenRouter free-model fallback chain

Use this when a user wants Hermes configured to prefer free OpenRouter models and automatically fail over when one hits rate limits.

## Durable takeaways

- Hermes supports a top-level `fallback_providers:` list in `~/.hermes/config.yaml`.
- Each entry is a dict like:

```yaml
- provider: openrouter
  model: openai/gpt-oss-120b:free
```

- Hermes tries fallback entries in order when the primary model fails with rate-limit, overload, or connection errors.
- CLI helper: `hermes fallback list|add|remove|clear`
- OpenRouter's live model catalog is at `https://openrouter.ai/api/v1/models`.
- A practical way to identify currently free models is to filter for models whose numeric `pricing` fields are all zero.
- Do not assume `:free` models are equally stable. Some can be temporarily rate-limited upstream even when they remain listed as free.
- For users who want strongest-first routing, rank primarily by likely capability, but keep at least one broad fallback such as `openrouter/free` near the end.

## Example strongest-first text fallback chain

Primary:

```yaml
model:
  provider: openrouter
  default: qwen/qwen3-coder:free
  context_length: 1048576
```

Fallbacks:

```yaml
fallback_providers:
  - provider: openrouter
    model: openai/gpt-oss-120b:free
  - provider: openrouter
    model: nvidia/nemotron-3-super-120b-a12b:free
  - provider: openrouter
    model: qwen/qwen3-next-80b-a3b-instruct:free
  - provider: openrouter
    model: z-ai/glm-4.5-air:free
  - provider: openrouter
    model: google/gemma-4-31b-it:free
  - provider: openrouter
    model: meta-llama/llama-3.3-70b-instruct:free
  - provider: openrouter
    model: google/gemma-4-26b-a4b-it:free
  - provider: openrouter
    model: openrouter/free
```

## Good operating pattern

1. Query the live OpenRouter catalog instead of relying on memory.
2. Filter free models from live pricing.
3. Prefer models that advertise tool/function calling support for Hermes agent use.
4. For multimodal fallbacks, include models with `image`/`video` input modalities if the user explicitly wants non-text coverage.
5. Verify the final chain with `hermes fallback list` after writing config.
6. Warn the user that a fresh Hermes session or gateway restart may be needed for the new routing to take effect.

## Pitfalls

- `OPENROUTER_API_KEY` may exist in Hermes-managed env while not being inherited by arbitrary shell subprocesses. For direct shell/API probes, source `~/.hermes/.env` first if needed.
- A model being free in the catalog does not mean it is available at that moment; transient upstream 429s are common on free tiers.
- Some free models may technically answer but produce poor instruction-following quality; keep a quality-first ordering for the first few fallback slots.
- Multimodal/audio-capable models should not automatically replace text-primary models unless the user asked for that behavior.
