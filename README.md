# Hermes Agent Sam Public Restore Kit

This repository is a public-safe restore kit for a Hermes Agent setup.
It is designed for bootstrapping a new server after Hermes Agent and an LLM provider are installed.

## What is included

- Sanitized Hermes config: `backup/config/config.yaml.sanitized`
- Environment variable template: `backup/config/env.example`
- Public-safe built-in memory files, if present: `backup/memory/`
- Public-safe installed skills copied from `~/.hermes/skills/`: `backup/skills/`
- Idempotent restore script: `scripts/restore-hermes-backup.py`
- Reusable backup refresh script: `scripts/create-hermes-public-backup.py`
- Manifest with source paths, counts, and exclusions: `backup/manifest.json`

## What is deliberately excluded

This repository is public. It must not contain secrets or private runtime data.
Excluded items include `.env`, `auth.json`, API keys, OAuth refresh tokens, passwords, private keys, browser profiles, cookies, raw session transcripts, raw databases, logs, generated media, caches, and virtual environments.

If you need a full secret-bearing backup, store it only in a private encrypted location using your own passphrase or secret manager. Do not place it in this public repo.

## Quick restore

```bash
git clone https://github.com/samlaggz/hermes-agent-sam.git
cd hermes-agent-sam
python3 scripts/restore-hermes-backup.py --include-memory
hermes config check
hermes doctor
hermes memory status
hermes skills list
```

Then manually fill secrets in `~/.hermes/.env`, run `hermes login`, or use `hermes auth add` as needed.

Last refreshed: 2026-05-21T07:40:29Z
