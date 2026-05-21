# Restore Instructions

These steps assume Hermes Agent is already installed on the new server and an LLM/provider is configured enough to run Hermes.

## 1. Clone the public-safe backup repo

```bash
git clone https://github.com/samlaggz/hermes-agent-sam.git
cd hermes-agent-sam
```

## 2. Run the restore script

Restore config and skills only:

```bash
python3 scripts/restore-hermes-backup.py
```

Restore config, skills, and public-safe built-in memory files:

```bash
python3 scripts/restore-hermes-backup.py --include-memory
```

The script is idempotent. Before modifying anything, it backs up existing `~/.hermes/config.yaml`, `~/.hermes/MEMORY.md`, `~/.hermes/USER.md`, and `~/.hermes/skills/` to:

```text
~/.hermes/restore-backups/<timestamp>/
```

## 3. Add private secrets manually

This public repo never restores real secrets. Fill them manually in:

```text
~/.hermes/.env
```

or use:

```bash
hermes login
hermes auth add
hermes model
hermes memory setup
hermes honcho setup
```

Use `backup/config/env.example` or the generated `~/.hermes/.env.example.from-backup` as a checklist.

## 4. Verify the restore

```bash
hermes config check
hermes doctor
hermes memory status
hermes skills list
```

If tools, skills, or config changes do not appear in an already-running Hermes session, start a fresh session or use `/reset`. For gateway use, restart the gateway.

## Honcho notes

Raw Honcho databases and API credentials are excluded. Reconnect Honcho using your private credentials, then run `hermes memory status` to verify.
