# Hermes Agent Sam Public Restore Kit

This repository is a public-safe restore kit for a Hermes Agent setup.
It is designed for bootstrapping a new server after Hermes Agent and an LLM provider are installed.

## SEO / repo purpose

Hermes Agent restore kit for **unblocked and unrestricted browsing workflows** on authorized websites, with or without GUI: Browser Use, live CDP Chromium, self-hosted watchable browser sessions, headless/non-GUI web browsing, web automation, CAPTCHA-aware browsing procedures, blocked-site diagnostics, and video-production skills. Credentials, cookies, browser profiles, and private runtime data are deliberately excluded.

## What is included

- Sanitized Hermes config: `backup/config/config.yaml.sanitized`
- Environment variable template: `backup/config/env.example`
- Public-safe built-in memory files, if present: `backup/memory/`
- Public-safe installed skills copied from `~/.hermes/skills/`: `backup/skills/`
- Browser/browsing skills for GUI and non-GUI web access workflows, including Browser Use MCP/cloud orchestration, live CDP browser sessions, CAPTCHA-aware browsing, blocked-site diagnostics, and self-hosted visible browser workflows.
- Video and creative production skills for stock-video sourcing, high-beat real-estate teasers, Magnific workflows, MiniMax Hailuo/Kling prompting, ComfyUI, Manim, TouchDesigner, and related editing/provenance workflows.
- Idempotent restore script: `scripts/restore-hermes-backup.py`
- Reusable backup refresh script: `scripts/create-hermes-public-backup.py`
- Manifest with source paths, counts, and exclusions: `backup/manifest.json`

## Browser and video capability note

With the restored tools, MCP configuration, and skills, Hermes can work with websites through both GUI and non-GUI paths:

- **GUI browser access:** visible Chromium/CDP sessions, live browser workflows, Browser Use Cloud sessions, noVNC/live-view style workflows, and screenshot/vision-assisted interaction when enabled and authenticated privately.
- **Non-GUI browsing:** web/search extraction, HTTP/API workflows, terminal-based fetch/curl patterns, and MCP tool calls for browser orchestration.
- **Robust browsing procedures:** CAPTCHA-aware handling, blocked-site diagnostics, profile/session guidance, and safe fallback strategies.
- **Video workflows:** stock b-roll keywording, source provenance, clip trimming/cropping guidance, branded outro guidance, AI video prompting, and local/remote rendering workflows.

No browser cookies, profiles, API keys, login tokens, provider credentials, generated videos, or private project media are stored in this public repo. Add credentials only on the private target machine via `~/.hermes/.env`, `hermes login`, or `hermes auth add`.

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

Last refreshed: 2026-05-21T10:07:04Z
