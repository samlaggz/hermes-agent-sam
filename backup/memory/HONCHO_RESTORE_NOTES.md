# Honcho Restore Notes

This public backup includes only sanitized Hermes memory/config files. It does not include raw Honcho databases, Honcho API keys, OAuth tokens, embeddings, transcripts, or other private memory-provider state.

On a new server:

1. Install and configure Hermes Agent.
2. Put private Honcho credentials in `~/.hermes/.env` or configure them via the normal Hermes setup flow.
3. Run `hermes memory setup` or `hermes honcho setup` as appropriate for your installation.
4. Verify with `hermes memory status`.

If you need a full Honcho export, store it only in a private encrypted backup, not in this public repository.
