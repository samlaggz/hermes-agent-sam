#!/usr/bin/env python3
"""Restore a public-safe Hermes Agent backup kit.

Idempotent behavior:
- Detects repository root.
- Backs up existing config, memory, and skills before modifying.
- Merges sanitized config without overwriting existing secret-looking values.
- Copies public-safe skills.
- Copies memory only when --include-memory is passed.
- Writes an env template, never fake secrets.
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import shutil
import stat
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None

SECRET_KEY_RE = re.compile(r"(?i)(secret|token|password|passwd|api[_-]?key|access[_-]?key|auth|credential|client[_-]?secret|refresh[_-]?token|private[_-]?key|cookie|session|bearer)")
REDACTED_MARKERS = {"<REDACTED_PUBLIC_BACKUP>", "<SET_IN_PRIVATE_ENV>", "REDACTED", "***"}


def now_stamp() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in [here.parent, *here.parents]:
        if (p / "backup" / "manifest.json").exists() and (p / "scripts" / "restore-hermes-backup.py").exists():
            return p
    raise SystemExit("Could not detect repo root containing backup/manifest.json")


def backup_path(src: Path, backup_dir: Path) -> None:
    if not src.exists():
        return
    dest = backup_dir / src.name
    if src.is_dir():
        shutil.copytree(src, dest, dirs_exist_ok=True)
    else:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)


def is_redacted_value(v: Any) -> bool:
    return isinstance(v, str) and (v.strip() in REDACTED_MARKERS or "REDACTED_PUBLIC_BACKUP" in v or "SET_IN_PRIVATE_ENV" in v)


def merge_config(existing: Any, incoming: Any, key_path: str = "") -> Any:
    if existing is None:
        return incoming
    if isinstance(existing, dict) and isinstance(incoming, dict):
        result = dict(existing)
        for k, v in incoming.items():
            path = f"{key_path}.{k}" if key_path else str(k)
            if k in result:
                result[k] = merge_config(result[k], v, path)
            else:
                result[k] = v
        return result
    leaf = key_path.split(".")[-1]
    if SECRET_KEY_RE.search(leaf):
        if existing not in (None, "", False) and is_redacted_value(incoming):
            return existing
        if incoming in (None, "", False) or is_redacted_value(incoming):
            return existing
    if is_redacted_value(incoming) and existing not in (None, ""):
        return existing
    return incoming


def restore_config(src: Path, dst: Path) -> str:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if yaml is None:
        if not dst.exists():
            shutil.copy2(src, dst)
            return "copied sanitized config (PyYAML unavailable; no existing config)"
        return "left existing config unchanged (PyYAML unavailable)"
    incoming = yaml.safe_load(src.read_text(encoding="utf-8")) if src.exists() else None
    existing = yaml.safe_load(dst.read_text(encoding="utf-8")) if dst.exists() else None
    merged = merge_config(existing, incoming)
    dst.write_text(yaml.safe_dump(merged, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return "merged sanitized config without overwriting existing secrets"


def copytree_overlay(src: Path, dst: Path) -> int:
    count = 0
    if not src.exists():
        return count
    for root, dirs, files in os.walk(src):
        rel_root = Path(root).relative_to(src)
        for d in dirs:
            (dst / rel_root / d).mkdir(parents=True, exist_ok=True)
        for f in files:
            s = Path(root) / f
            d = dst / rel_root / f
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(s, d)
            count += 1
    return count


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hermes-home", default=os.environ.get("HERMES_HOME", str(Path.home() / ".hermes")))
    ap.add_argument("--include-memory", action="store_true", help="restore public-safe MEMORY.md and USER.md files")
    args = ap.parse_args()

    root = find_repo_root()
    backup = root / "backup"
    hermes_home = Path(args.hermes_home).expanduser().resolve()
    hermes_home.mkdir(parents=True, exist_ok=True)

    backup_dir = hermes_home / "restore-backups" / now_stamp()
    backup_dir.mkdir(parents=True, exist_ok=True)
    for item in ("config.yaml", "MEMORY.md", "USER.md", "skills"):
        backup_path(hermes_home / item, backup_dir)

    messages = [f"Existing Hermes files backed up to {backup_dir}"]
    messages.append(restore_config(backup / "config" / "config.yaml.sanitized", hermes_home / "config.yaml"))

    env_src = backup / "config" / "env.example"
    if env_src.exists():
        shutil.copy2(env_src, hermes_home / ".env.example.from-backup")
        messages.append("wrote ~/.hermes/.env.example.from-backup (template only, no values)")

    skills_count = copytree_overlay(backup / "skills", hermes_home / "skills")
    messages.append(f"copied/updated {skills_count} public-safe skill files")

    if args.include_memory:
        mem_count = 0
        for name in ("MEMORY.md", "USER.md"):
            src = backup / "memory" / name
            if src.exists():
                shutil.copy2(src, hermes_home / name)
                mem_count += 1
        messages.append(f"restored {mem_count} public-safe memory files")
    else:
        messages.append("memory files not restored; rerun with --include-memory to restore public-safe MEMORY.md/USER.md")

    for line in messages:
        print(line)
    print("Next: fill private secrets manually in ~/.hermes/.env, or run hermes login / hermes auth add.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
