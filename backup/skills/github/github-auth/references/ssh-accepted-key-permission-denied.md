# SSH `Server accepts key` but GitHub returns `Permission denied (publickey)`

Use this when GitHub SSH auth behaves inconsistently: verbose SSH says the server accepted the offered key, but `ssh -T git@github.com` or `git ls-remote` still fails.

## Durable lesson

Do **not** treat `Server accepts key` as proof that the current key can push to the target repository. GitHub may know the key while it still does not grant the identity/repo access needed for the operation.

Common causes:

- The public key is attached to a different GitHub account than the repo owner/collaborator.
- The key is attached as an SSH signing key, not an authentication key.
- The key is already used as a deploy key on another repository.
- The key authenticates an account that lacks access to the target repo.
- The private key is passphrase-protected and the current non-interactive environment lacks an ssh-agent/passphrase.

## Diagnostic sequence

```bash
# Safe inventory: public keys only
ls -l ~/.ssh/*.pub 2>/dev/null
ssh-keygen -lf ~/.ssh/id_ed25519.pub 2>/dev/null || true

# Check gh/token/credential auth separately
gh auth status 2>/dev/null || echo "gh not authenticated"
test -n "$GITHUB_TOKEN" && echo "GITHUB_TOKEN present" || echo "GITHUB_TOKEN absent"
git config --global credential.helper 2>/dev/null || echo "no global credential helper"

# Verbose SSH with the intended key
ssh -vvv -o BatchMode=yes -o IdentitiesOnly=yes -i ~/.ssh/id_ed25519 -T git@github.com

# Verify access to the specific repo, not just shell auth
GIT_SSH_COMMAND='ssh -o BatchMode=yes -o IdentitiesOnly=yes -i ~/.ssh/id_ed25519' \
  git ls-remote git@github.com:<owner>/<repo>.git HEAD

# Detect passphrase-protected key in non-interactive contexts
ssh-keygen -y -f ~/.ssh/id_ed25519 >/dev/null
```

If `ssh-keygen -y` reports `incorrect passphrase supplied`, the private key cannot be used non-interactively unless an ssh-agent is loaded or the passphrase is supplied via an approved interactive flow.

## Preferred fix for public/repo restore-kit pushes

Create a fresh repo-specific deploy key instead of fighting ambiguous account-level key state:

```bash
KEY=~/.ssh/<repo>-deploy-ed25519
ssh-keygen -t ed25519 -C "<repo>-deploy-$(hostname)-$(date -u +%Y%m%d)" -f "$KEY" -N ""
chmod 600 "$KEY"
cat "$KEY.pub"
ssh-keygen -lf "$KEY.pub"
```

Ask the user to add the public key at:

```text
https://github.com/<owner>/<repo>/settings/keys
```

Important: enable **Allow write access**.

Then verify and push with the explicit key:

```bash
GIT_SSH_COMMAND="ssh -o BatchMode=yes -o IdentitiesOnly=yes -i $KEY" \
  git ls-remote git@github.com:<owner>/<repo>.git HEAD

GIT_SSH_COMMAND="ssh -o BatchMode=yes -o IdentitiesOnly=yes -i $KEY" \
  git push origin main
```

## Public backup safety reminder

For public restore-kit repositories, auth troubleshooting must stay separate from content safety. Do not commit `.env`, tokens, cookies, browser profiles, raw session databases, logs, caches, or media while solving GitHub auth.
