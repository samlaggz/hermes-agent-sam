# Clean re-embedding/reset for self-hosted Honcho after an embedding-model change

Use this when Honcho is already running with populated `documents` / `message_embeddings` tables and you want all stored vectors to be regenerated under the new embedding model only.

## When this is needed

Typical trigger:
- you switched embedding model family or dimensions behavior
- the database already contains old vectors
- `scripts/configure_embeddings.py --yes` refuses to alter populated tables

Example refusal pattern:
- `refusing to ALTER populated embedding tables ... Re-embed out-of-band into a fresh deployment, then cut over.`

## Safe non-destructive pattern first

If the target model supports output-dimension control (for example `text-embedding-3-small`), first consider matching the existing schema dimension instead of changing pgvector dimensions in-place.

Working pattern used successfully:
- keep `EMBEDDING_VECTOR_DIMENSIONS=768`
- set `EMBEDDING_MODEL_CONFIG__MODEL=text-embedding-3-small`
- set `EMBEDDING_MODEL_CONFIG__DIMENSIONS_MODE=always`
- verify an actual embedding call returns 768 dimensions before restart

This avoids immediate schema churn and lets you migrate content cleanly.

## Clean reset workflow

1. Back up the embedding-bearing tables before deletion.
2. Stop `honcho-api` and `honcho-deriver`.
3. Delete rows from:
   - `documents`
   - `message_embeddings`
4. Start the services again.
5. Regenerate message embeddings with:
   - `python scripts/generate_message_embeddings.py --batch-size 50`
6. Seed a fresh Hermes/Honcho memory write so deriver can rebuild new `documents` from scratch.
7. Verify counts and recall.

## Concrete commands

```bash
backup_dir=/root/honcho/backups
mkdir -p "$backup_dir"
stamp=$(date +%Y%m%d_%H%M%S)
backup_file="$backup_dir/honcho_embeddings_before_reset_${stamp}.sql"

sudo -u postgres pg_dump -d postgres -t public.documents -t public.message_embeddings > "$backup_file"

systemctl stop honcho-api honcho-deriver

sudo -u postgres psql -d postgres -v ON_ERROR_STOP=1 <<'SQL'
BEGIN;
DELETE FROM documents;
DELETE FROM message_embeddings;
COMMIT;
SQL

systemctl start honcho-api honcho-deriver
cd /root/honcho
./.venv/bin/python scripts/generate_message_embeddings.py --batch-size 50
```

## Verification

Check health:
```bash
curl http://127.0.0.1:8000/health
hermes honcho status
```

Check counts:
```bash
sudo -u postgres psql -d postgres -Atqc \
  "select 'messages='||count(*) from messages; \
    select 'message_embeddings='||count(*) from message_embeddings; \
    select 'documents='||count(*) from documents;"
```

Then force fresh derivation with a new memory write through Hermes and re-check counts. Expected pattern:
- immediately after reset/regeneration: `message_embeddings` restored, `documents` may be `0`
- after a fresh write and deriver pass: `documents` begins growing again

## Durable lesson

When changing Honcho embedding models on a populated deployment, the reusable lesson is not the transient schema error itself. The durable lesson is:
- prefer a dimension-compatible managed model configuration when possible
- otherwise do a backup + clear + regenerate cycle so every stored vector belongs to the new model family only
