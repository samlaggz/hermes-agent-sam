---
name: independent-background-agents
description: Launch long-running Hermes agent jobs independently from the messaging gateway, with per-job model/provider pinning, logs, and restart-safe lifecycle management.
version: 1.0.0
author: <REDACTED_PUBLIC_BACKUP>
license: MIT
created_by: agent
---

# Independent Background Agents

Use this when a user asks for long-running background work that must survive gateway restarts, model switches in the live chat, or messaging-platform interruptions.

## Triggers

- User says background tasks should keep running if `hermes gateway restart` or `/restart` happens.
- User wants different background tasks assigned to different LLM models/providers.
- User changes the plan mid-run and wants a new model used for the continuation.
- A task is expected to run for many minutes/hours and should have auditable logs.

## Core rule

Do **not** launch durable background jobs as children of the Telegram gateway process. Gateway-bound process managers are convenient for short work, but their children can be killed when the gateway restarts.

For durable work, launch a separate OS-level service, usually with `systemd-run`, and pin the provider/model in the command itself.

## Recommended systemd pattern

1. Write a self-contained prompt file.
2. Start a named transient service:

```bash
systemd-run \
  --unit hermes-task-NAME \
  --description "Hermes independent task NAME" \
  --working-directory /path/to/workdir \
  --property Restart=no \
  --property StandardOutput=append:/root/.hermes/independent_tasks/logs/NAME.log \
  --property StandardError=append:/root/.hermes/independent_tasks/logs/NAME.log \
  hermes chat -Q --pass-session-id \
    --source independent:NAME \
    --provider openai-codex \
    -m gpt-5.5 \
    -s skill-one,skill-two \
    -t terminal,file,web,skills,messaging \
    -q "$(cat /path/to/prompt.txt)"
```

3. Report the unit and log path:

```bash
systemctl status hermes-task-NAME --no-pager
tail -f /root/.hermes/independent_tasks/logs/NAME.log
```

4. To stop or supersede:

```bash
systemctl stop hermes-task-NAME
systemctl reset-failed hermes-task-NAME
```

## Model changes and plan changes

A running Hermes process does not hot-swap its LLM model. If the user changes the plan or model:

1. decide whether the old job should keep running or be stopped,
2. start a new independent job with a new unit name,
3. pass explicit `--provider` and `-m` flags,
4. if appropriate, resume the previous Hermes session with `--resume SESSION_ID` while using the new model flags.

## Supporting services are part of the background job

When the job depends on live infrastructure, make the **whole stack** gateway-independent, not just the final agent process. Long-running Magnific/browser/video jobs may depend on a dashboard, public tunnel, noVNC desktop stack, CDP Chromium, and local file server; start those as named `hermes-*` systemd units too. After a gateway restart, verify with `systemctl list-units 'hermes-*'` plus port checks before telling the user the run is restored.

See `references/gateway-independent-service-stack.md` for a compact restart/restore checklist.

For public/shared Git backup jobs — especially backing up Hermes settings, Honcho/memory, and skills — use `references/public-safe-hermes-backup-jobs.md`. It defines the safe restore-kit shape, required exclusions, secret scans, and final report fields. Treat public repos as hostile by default: never commit `.env`, auth files, raw cookies/browser profiles, OAuth tokens, raw session databases, or secret-bearing Honcho exports.

## Practical helper

On this Hermes instance, the helper `/root/.hermes/scripts/hermes_independent_task.py` may be available. It wraps the systemd pattern:

```bash
/root/.hermes/scripts/hermes_independent_task.py start \
  --name my-job \
  --provider openai-codex \
  --model gpt-5.5 \
  --skills skill-one,skill-two \
  --toolsets terminal,file,web,skills,messaging \
  --workdir /path/to/workdir \
  --prompt-file /path/to/prompt.txt
```

Lifecycle:

```bash
/root/.hermes/scripts/hermes_independent_task.py list
/root/.hermes/scripts/hermes_independent_task.py status my-job
/root/.hermes/scripts/hermes_independent_task.py log my-job --lines 120
/root/.hermes/scripts/hermes_independent_task.py stop my-job
```

## Pitfalls

- Do not infer that `process list` showing empty means no independent tasks exist; systemd tasks are checked with `systemctl list-units 'hermes-task-*'` or the helper's `list` command.
- Do not rely on the live chat model for background workers. Always pin the job's model/provider explicitly.
- Do not claim a background task delivered final output unless the logs or returned files verify it.
- Use a new unit/log name for major plan changes to keep audit trails clear.
