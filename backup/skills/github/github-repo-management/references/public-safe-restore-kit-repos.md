# Public-safe restore-kit repositories

Use this pattern when the user wants to back up an agent/dev environment into a public GitHub repository so a fresh install can restore settings, skills, and notes.

## Rule of thumb

A public restore kit should be **reproducible**, not a raw home-directory backup. Commit scripts, docs, manifests, sanitized config examples, and non-secret skills. Never commit live credentials or secret-bearing state.

## Include

- `README.md` with purpose, safety model, and quick restore commands.
- `RESTORE.md` or equivalent detailed restore guide.
- `scripts/restore-*.py` or `.sh` scripts that copy files into the target install with backups.
- `scripts/create-*.py` or `.sh` scripts for future sanitized refreshes.
- Sanitized config examples with variable names/placeholders only.
- Skills content that is safe to share.
- Memory/Honcho notes only when sanitized and intentionally exportable.
- `manifest.json` or `MANIFEST.md` listing what was included/excluded and source paths.

## Exclude

- `.env`, API keys, tokens, passwords, OAuth refresh tokens, Telegram bot tokens, ngrok tokens, GitHub tokens.
- `auth.json`, cookies, browser profiles/sessions, credential stores.
- Raw session transcripts, raw databases, raw vector stores with private content.
- Logs, caches, temporary directories, binaries, generated media, and downloaded assets.
- Private SSH keys or GPG secret keys.

## Workflow

1. Treat the destination visibility as public even if the user is unsure.
2. Stage restore-kit files in a clean workdir, not directly from the live config directory.
3. Generate config examples from allowlists of keys, not by copying full config files and redacting after the fact.
4. Add explicit `.gitignore` deny rules for secret/state patterns before any `git add`.
5. Before committing, inspect staged files:

```bash
git status --short
git diff --cached --stat
git diff --cached --name-only
```

6. Run lightweight secret scans over staged content. At minimum search for common names and token-shaped strings:

```bash
git diff --cached | grep -Ei 'token|secret|password|api[_-]?key|refresh|cookie|authorization' || true
```

7. Commit locally first. Push only after GitHub auth is verified.
8. After push, verify the remote content and re-check that no secret-bearing paths were uploaded.

## Restore UX target

The repo should let a fresh machine do something like:

```bash
git clone https://github.com/<owner>/<repo>.git
cd <repo>
python3 scripts/restore-hermes-backup.py --include-memory
hermes config check
hermes doctor
hermes skills list
```

Use placeholders and post-restore instructions for credentials that must be re-entered manually.

## Auth separation pitfall

Website logins/cookies from unrelated browser tasks cannot authorize GitHub pushes. GitHub push requires a GitHub-specific auth path: PAT, `gh auth`, account SSH key with repo access, or repo deploy key with write access.
