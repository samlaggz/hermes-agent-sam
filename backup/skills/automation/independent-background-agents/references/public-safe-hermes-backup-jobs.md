# Public-safe Hermes backup jobs

Use this when a user asks to back up Hermes settings, Honcho/memory, and skills into a public or shared Git repository, especially as a durable background task.

## Goal shape

Create a restore kit that a fresh Hermes install can consume after the user sets up an LLM and provides the repo URL. The kit should restore non-secret configuration, skills, and memory notes without exposing credentials.

## Include

- `README.md` and `RESTORE.md` with exact fresh-install restore steps.
- `scripts/restore-hermes-backup.py` that is idempotent and backs up existing local files before modifying `~/.hermes`.
- `scripts/create-hermes-public-backup.py` so the backup can be refreshed safely later.
- Sanitized `config.yaml` preserving structure and non-secret settings.
- `.env.example` with variable names/placeholders only.
- Built-in `MEMORY.md` / `USER.md` only after scanning and redacting secret-like values.
- Honcho restore notes and sanitized provider configuration; do not export raw Honcho databases or API credentials to a public repo.
- Installed skills under `~/.hermes/skills/`, excluding caches, `.git`, virtualenvs, binaries, large media, and generated artifacts.
- A manifest with timestamp, source paths, file counts, and exclusions.

## Exclude from public repos

Never commit:

- `.env`, `auth.json`, OAuth refresh tokens, credential pools.
- API keys, passwords, provider tokens, Telegram/Discord bot tokens, GitHub tokens, ngrok/tunnel tokens.
- Browser profiles, cookies, local storage, session cookies, Magnific/login credentials.
- Raw session transcripts or databases that may contain PII/secrets.
- Private keys or files containing `BEGIN PRIVATE KEY`.

## Required scans before commit

At minimum search for obvious secret indicators before committing:

- filenames: `.env`, `auth.json`, `credentials`, `cookie`, `token`, `secret`, `private_key`;
- content markers: `BEGIN PRIVATE KEY`, `refresh_token`, `client_secret`, `api_key`, `password:`, `token:`, `TELEGRAM`, `OPENAI`, `ANTHROPIC`, `GITHUB_TOKEN`, `ngrok`;
- high-entropy key-like strings where practical.

If anything looks suspicious, redact or exclude it before commit. Do not include secret values in logs or the final user response.

## Background job prompt requirements

For a durable independent background job, the prompt should be self-contained and specify:

1. target repo URL and working directory;
2. public-safe constraint and exact exclusions;
3. expected files/scripts to create;
4. secret scan requirement;
5. commit/push behavior and fallback if authentication fails;
6. final report fields: push success, commit hash, repo URL, included/excluded summary, restore command.

Pin provider/model and use a dedicated unit/log name so the job is auditable and survives gateway restarts.