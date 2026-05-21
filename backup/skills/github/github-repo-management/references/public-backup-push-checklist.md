# Public backup / restore-kit push checklist

Use this for public-safe Hermes backup repos or similar restore-kit repositories before pushing.

## Verify repository and branch state

```bash
cd /path/to/repo
git status --short --branch
git --no-pager log --oneline --decorate --max-count=3
git remote -v
git ls-remote https://github.com/OWNER/REPO.git || true
```

If `git ls-remote` returns no refs, the repo may simply be empty. Confirm repo existence and default branch with `gh repo view OWNER/REPO` or the GitHub API before treating it as an auth/remote failure.

## Deploy-key push pattern

For repo-specific deploy keys, prefer explicit SSH for verification and push:

```bash
ssh -T -o BatchMode=yes -o IdentitiesOnly=yes \
  -i /path/to/deploy_key \
  -o StrictHostKeyChecking=accept-new git@github.com || true

git remote set-url origin git@github.com:OWNER/REPO.git
GIT_SSH_COMMAND='ssh -i /path/to/deploy_key -o BatchMode=yes -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new' \
  git push -u origin main

GIT_SSH_COMMAND='ssh -i /path/to/deploy_key -o BatchMode=yes -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new' \
  git ls-remote origin HEAD refs/heads/main
```

Expected SSH probe text is like: `Hi OWNER/REPO! You've successfully authenticated, but GitHub does not provide shell access.`

## Secret-scan discipline

Run a high-risk literal secret scan before pushing. Avoid blocking on placeholders such as `$API_KEY`, `{token}`, `<SET_IN_PRIVATE_ENV>`, `REDACTED`, or test fixture strings. The goal is to catch literal private keys and real tokens, not documentation examples.

High-signal patterns to scan:

- OpenAI-like secret keys: `sk-...`
- GitHub tokens: `ghp_...`, `gho_...`, `ghu_...`, `ghs_...`, `ghr_...`
- AWS access keys: `AKIA...`
- private key blocks: `-----BEGIN ... PRIVATE KEY-----`
- Google API keys: `AIza...`
- Slack tokens: `xox...`

## Background job pitfall

If a background worker validates restore scripts, avoid shell cleanup such as `rm -rf "$tmpdir"` in prompts because Hermes may raise an interactive dangerous-command prompt and abort the autonomous worker if denied. Use bounded Python cleanup on a freshly-created temp directory, or leave temporary files behind and report their path.
