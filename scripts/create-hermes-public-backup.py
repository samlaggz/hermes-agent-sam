#!/usr/bin/env python3
"""Create a public-safe Hermes Agent backup/restore kit.

This script intentionally excludes secrets, auth files, raw sessions, browser
profiles, cookies, databases, caches, binaries, generated media, and other
high-risk artifacts. Text files that are copied are scanned and obvious secret
values are redacted.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import stat
import sys
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None

SECRET_KEY_RE = re.compile(
    r"(?i)(secret|token|password|passwd|api[_-]?key|access[_-]?key|auth|credential|client[_-]?secret|refresh[_-]?token|private[_-]?key|cookie|session|bearer)"
)
SECRET_VALUE_RE = re.compile(
    r"(?i)(sk-[A-Za-z0-9_-]{16,}|gh[pousr]_[A-Za-z0-9_]{20,}|xox[baprs]-[A-Za-z0-9-]{20,}|AIza[0-9A-Za-z_-]{20,}|ya29\.[0-9A-Za-z_-]+|eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|Bearer\s+[A-Za-z0-9._~+/=-]{16,})"
)
ENV_ASSIGN_RE = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=")
CONFIG_ENV_REF_RE = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")
LINE_SECRET_RE = re.compile(r"(?i)^([ \t]*[A-Za-z0-9_.-]*(secret|token|password|passwd|api[_-]?key|auth|credential|client[_-]?secret|refresh[_-]?token|private[_-]?key|cookie|session)[A-Za-z0-9_.-]*[ \t]*[:=][ \t]*).+$")

EXCLUDE_NAMES = {
    ".git", ".hg", ".svn", "node_modules", "__pycache__", ".pytest_cache",
    ".mypy_cache", ".ruff_cache", ".cache", "cache", "caches", ".venv", "venv",
    "env", "dist", "build", "target", ".tox", ".DS_Store", "auth.json", ".env",
    ".hub", "index-cache", "cookies", "cookie", "Cookie", "Cookies", "browser_profiles", "profiles",
    "sessions", "session", "logs", "log", "databases", "db", "tmp", "temp",
}
EXCLUDE_SUFFIXES = {
    ".sqlite", ".sqlite3", ".db", ".db-wal", ".db-shm", ".log", ".pem", ".key",
    ".crt", ".p12", ".pfx", ".zip", ".tar", ".gz", ".tgz", ".7z", ".rar",
    ".mp4", ".mov", ".mkv", ".webm", ".avi", ".mp3", ".wav", ".flac", ".ogg",
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".heic", ".ico", ".pdf",
    ".bin", ".pt", ".pth", ".safetensors", ".onnx", ".gguf",
}
MAX_TEXT_BYTES = 2_000_000
REDACTED = "<REDACTED_PUBLIC_BACKUP>"
PLACEHOLDER = "<SET_IN_PRIVATE_ENV>"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def now_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def ensure_clean_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def is_binary_bytes(data: bytes) -> bool:
    return b"\0" in data[:4096]


def should_exclude_path(path: Path) -> tuple[bool, str | None]:
    parts = set(path.parts)
    for name in EXCLUDE_NAMES:
        if name in parts or path.name == name:
            return True, f"excluded name: {name}"
    if path.suffix.lower() in EXCLUDE_SUFFIXES:
        return True, f"excluded suffix: {path.suffix}"
    return False, None


def sanitize_text(text: str) -> str:
    text = SECRET_VALUE_RE.sub(REDACTED, text)
    out = []
    for line in text.splitlines():
        m = LINE_SECRET_RE.match(line)
        if m:
            out.append(m.group(1) + REDACTED)
        else:
            out.append(line)
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")


def sanitize_obj(obj: Any, path: str = "") -> Any:
    if isinstance(obj, dict):
        new = {}
        for k, v in obj.items():
            key = str(k)
            full = f"{path}.{key}" if path else key
            if SECRET_KEY_RE.search(key):
                if isinstance(v, (dict, list)):
                    new[k] = sanitize_obj(v, full)
                elif v in (None, "", False):
                    new[k] = v
                else:
                    new[k] = REDACTED
            else:
                new[k] = sanitize_obj(v, full)
        return new
    if isinstance(obj, list):
        return [sanitize_obj(v, path) for v in obj]
    if isinstance(obj, str):
        return SECRET_VALUE_RE.sub(REDACTED, obj)
    return obj


def write_sanitized_config(src: Path, dst: Path) -> tuple[bool, list[str]]:
    env_refs: set[str] = set()
    if not src.exists():
        dst.write_text("# No ~/.hermes/config.yaml found on source machine.\n", encoding="utf-8")
        return False, []
    raw = src.read_text(encoding="utf-8", errors="replace")
    env_refs.update(CONFIG_ENV_REF_RE.findall(raw))
    if yaml is not None:
        try:
            data = yaml.safe_load(raw)
            data = sanitize_obj(data)
            dst.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
            return True, sorted(env_refs)
        except Exception:
            pass
    dst.write_text(sanitize_text(raw), encoding="utf-8")
    return True, sorted(env_refs)


def derive_env_names(hermes_home: Path, config_env_refs: list[str]) -> list[str]:
    names = set(config_env_refs)
    env_path = hermes_home / ".env"
    if env_path.exists():
        try:
            for line in env_path.read_text(encoding="utf-8", errors="replace").splitlines():
                m = ENV_ASSIGN_RE.match(line)
                if m:
                    names.add(m.group(1))
        except Exception:
            pass
    # Include common Hermes provider vars if referenced by sanitized config text or likely useful.
    common = [
        "OPENROUTER_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GOOGLE_API_KEY",
        "GEMINI_API_KEY", "DEEPSEEK_API_KEY", "GITHUB_TOKEN", "GROQ_API_KEY",
        "MISTRAL_API_KEY", "HF_TOKEN", "XAI_API_KEY", "DASHSCOPE_API_KEY",
        "KIMI_API_KEY", "GLM_API_KEY", "MINIMAX_API_KEY", "MINIMAX_CN_API_KEY",
        "VOICE_TOOLS_OPENAI_KEY", "HONCHO_API_KEY", "HONCHO_URL", "MCP_BROWSER_USE_API_KEY",
        "TELEGRAM_BOT_TOKEN", "NGROK_AUTHTOKEN",
    ]
    for n in common:
        if n in names:
            continue
    return sorted(names)


def copy_public_safe_tree(src: Path, dst: Path) -> dict[str, Any]:
    stats = {"files_copied": 0, "files_redacted": 0, "files_excluded": 0, "excluded_samples": []}
    if not src.exists():
        return stats
    for root, dirs, files in os.walk(src):
        root_path = Path(root)
        keep_dirs = []
        for d in dirs:
            p = root_path / d
            excluded, reason = should_exclude_path(p.relative_to(src))
            if excluded:
                stats["files_excluded"] += 1
                if len(stats["excluded_samples"]) < 50:
                    stats["excluded_samples"].append({"path": str(p.relative_to(src)), "reason": reason})
            else:
                keep_dirs.append(d)
        dirs[:] = keep_dirs
        for f in files:
            p = root_path / f
            rel = p.relative_to(src)
            excluded, reason = should_exclude_path(rel)
            if excluded:
                stats["files_excluded"] += 1
                if len(stats["excluded_samples"]) < 50:
                    stats["excluded_samples"].append({"path": str(rel), "reason": reason})
                continue
            try:
                if p.stat().st_size > MAX_TEXT_BYTES:
                    stats["files_excluded"] += 1
                    if len(stats["excluded_samples"]) < 50:
                        stats["excluded_samples"].append({"path": str(rel), "reason": "too large for public text backup"})
                    continue
                data = p.read_bytes()
                if is_binary_bytes(data):
                    stats["files_excluded"] += 1
                    if len(stats["excluded_samples"]) < 50:
                        stats["excluded_samples"].append({"path": str(rel), "reason": "binary file"})
                    continue
                text = data.decode("utf-8", errors="replace")
                sanitized = sanitize_text(text)
                out = dst / rel
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_text(sanitized, encoding="utf-8")
                shutil.copymode(p, out, follow_symlinks=False)
                stats["files_copied"] += 1
                if sanitized != text:
                    stats["files_redacted"] += 1
            except Exception as e:
                stats["files_excluded"] += 1
                if len(stats["excluded_samples"]) < 50:
                    stats["excluded_samples"].append({"path": str(rel), "reason": f"read/copy error: {e.__class__.__name__}"})
    return stats


def write_docs(root: Path, manifest: dict[str, Any]) -> None:
    (root / "README.md").write_text(f"""# Hermes Agent Sam Public Restore Kit

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

Last refreshed: {manifest.get('timestamp_utc', 'unknown')}
""", encoding="utf-8")

    (root / "RESTORE.md").write_text("""# Restore Instructions

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
""", encoding="utf-8")

    (root / ".gitignore").write_text("""# Secrets and credentials
.env
.env.*
!.env.example
**/.env
**/.env.*
auth.json
**/auth.json
*.pem
*.key
*.p12
*.pfx
*secret*
*token*
*credential*

# Runtime/private data
sessions/
logs/
*.log
*.sqlite
*.sqlite3
*.db
*.db-wal
*.db-shm
browser_profiles/
cookies/

# Generated/cache/dependencies
__pycache__/
*.pyc
node_modules/
.venv/
venv/
.cache/
.pytest_cache/
dist/
build/

# Media/binaries likely unsafe or huge for public backup
*.mp4
*.mov
*.mkv
*.webm
*.avi
*.mp3
*.wav
*.flac
*.png
*.jpg
*.jpeg
*.gif
*.webp
*.zip
*.tar
*.gz
*.tgz
*.7z
*.safetensors
*.gguf
""", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hermes-home", default=os.environ.get("HERMES_HOME", str(Path.home() / ".hermes")))
    args = ap.parse_args()

    root = repo_root()
    hermes_home = Path(args.hermes_home).expanduser().resolve()
    backup = root / "backup"
    ensure_clean_dir(backup)
    (backup / "config").mkdir(parents=True, exist_ok=True)
    (backup / "memory").mkdir(parents=True, exist_ok=True)
    (backup / "skills").mkdir(parents=True, exist_ok=True)

    timestamp = now_utc()
    config_found, config_env_refs = write_sanitized_config(hermes_home / "config.yaml", backup / "config" / "config.yaml.sanitized")

    env_names = derive_env_names(hermes_home, config_env_refs)
    env_text = "# Public-safe template generated from variable names only. Fill values privately.\n"
    for name in env_names:
        env_text += f"{name}={PLACEHOLDER}\n"
    (backup / "config" / "env.example").write_text(env_text, encoding="utf-8")

    memory_stats = {"files_copied": 0, "files_redacted": 0, "files_excluded": 0, "excluded_samples": []}
    for name in ("MEMORY.md", "USER.md"):
        src = hermes_home / name
        if src.exists():
            text = src.read_text(encoding="utf-8", errors="replace")
            san = sanitize_text(text)
            (backup / "memory" / name).write_text(san, encoding="utf-8")
            memory_stats["files_copied"] += 1
            if san != text:
                memory_stats["files_redacted"] += 1

    (backup / "memory" / "HONCHO_RESTORE_NOTES.md").write_text("""# Honcho Restore Notes

This public backup includes only sanitized Hermes memory/config files. It does not include raw Honcho databases, Honcho API keys, OAuth tokens, embeddings, transcripts, or other private memory-provider state.

On a new server:

1. Install and configure Hermes Agent.
2. Put private Honcho credentials in `~/.hermes/.env` or configure them via the normal Hermes setup flow.
3. Run `hermes memory setup` or `hermes honcho setup` as appropriate for your installation.
4. Verify with `hermes memory status`.

If you need a full Honcho export, store it only in a private encrypted backup, not in this public repository.
""", encoding="utf-8")

    skills_stats = copy_public_safe_tree(hermes_home / "skills", backup / "skills")

    manifest = {
        "timestamp_utc": timestamp,
        "public_safe": True,
        "source_paths": {
            "hermes_home": str(hermes_home),
            "config": str(hermes_home / "config.yaml"),
            "env": str(hermes_home / ".env (names only, values excluded)"),
            "memory": [str(hermes_home / "MEMORY.md"), str(hermes_home / "USER.md")],
            "skills": str(hermes_home / "skills"),
        },
        "included": {
            "config_found": config_found,
            "env_variable_names_count": len(env_names),
            "memory": memory_stats,
            "skills": skills_stats,
        },
        "exclusions": {
            "secret_files": [".env", "auth.json", "OAuth tokens", "API keys", "private keys", "cookies"],
            "runtime_private_data": ["raw session transcripts", "raw databases", "browser profiles", "logs"],
            "generated_or_large": sorted(EXCLUDE_SUFFIXES),
            "excluded_directory_names": sorted(EXCLUDE_NAMES),
        },
        "redaction_marker": REDACTED,
    }
    (backup / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (backup / "manifest.md").write_text(
        f"# Backup Manifest\n\n- Timestamp UTC: {timestamp}\n- Hermes home: `{hermes_home}`\n- Config found: {config_found}\n- Env variable names: {len(env_names)}\n- Memory files copied: {memory_stats['files_copied']}\n- Skill files copied: {skills_stats['files_copied']}\n- Skill files redacted: {skills_stats['files_redacted']}\n- Skill paths excluded/skipped: {skills_stats['files_excluded']}\n\nSee `manifest.json` for full details.\n",
        encoding="utf-8",
    )

    write_docs(root, manifest)
    for script in (root / "scripts").glob("*.py"):
        mode = script.stat().st_mode
        script.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    print(json.dumps({"ok": True, "repo": str(root), "timestamp_utc": timestamp, "skills_files": skills_stats["files_copied"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
