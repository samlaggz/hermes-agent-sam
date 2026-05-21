# Gateway-independent Hermes background tasks

Use this when a long-running Hermes job must survive `hermes gateway restart`, model switches, Telegram reconnects, or gateway crashes.

## Problem

Starting a long job with the gateway-bound terminal/process manager makes it a child of the gateway session. Restarting the gateway to pick up config/model changes can kill those children.

## Preferred pattern

Run the job as an OS-managed service (`systemd-run`) with its own pinned provider/model, workdir, skills, toolsets, and logs.

Minimal shape:

```bash
systemd-run \
  --unit hermes-task-NAME \
  --description 'Hermes independent task NAME' \
  --working-directory /path/to/workdir \
  --property Restart=no \
  --property StandardOutput=append:/root/.hermes/independent_tasks/logs/NAME.log \
  --property StandardError=append:/root/.hermes/independent_tasks/logs/NAME.log \
  /usr/bin/bash -lc 'hermes chat -Q --pass-session-id --source independent:NAME --provider PROVIDER -m MODEL -s SKILLS -t TOOLSETS -q "PROMPT"'
```

Manage it:

```bash
systemctl status hermes-task-NAME --no-pager
journalctl -u hermes-task-NAME -n 100 --no-pager
systemctl stop hermes-task-NAME
systemctl reset-failed hermes-task-NAME
```

## Local helper available in this environment

This user has a helper script at:

```bash
/root/.hermes/scripts/hermes_independent_task.py
```

Common commands:

```bash
/root/.hermes/scripts/hermes_independent_task.py start \
  --name magnific-v4 \
  --provider openai-codex \
  --model gpt-5.5 \
  --skills magnific-short-video-production,minimax-hailuo-23-json-prompting \
  --toolsets browser,terminal,file,vision,skills,todo,messaging \
  --workdir /tmp/horror_short_project \
  --prompt-file /tmp/prompt.txt \
  --replace

/root/.hermes/scripts/hermes_independent_task.py list
/root/.hermes/scripts/hermes_independent_task.py status magnific-v4
/root/.hermes/scripts/hermes_independent_task.py log magnific-v4 --lines 120
/root/.hermes/scripts/hermes_independent_task.py stop magnific-v4
```

To continue with a different model after a plan change, start a new service with a new `--provider`/`--model` and either point at the same project files or resume a specific Hermes session:

```bash
/root/.hermes/scripts/hermes_independent_task.py start \
  --name task-gpt55 \
  --provider openai-codex \
  --model gpt-5.5 \
  --resume-session SESSION_ID \
  --prompt 'Continue with the updated plan...'
```

## Rules

- Pin `--provider` and `-m/--model` per independent task. Do not rely on the current chat's model if the job may run for hours.
- Treat a plan/model change as a new process boundary: stop obsolete tasks or launch a replacement that resumes from the saved files/session.
- Write prompts to files for long instructions; avoid huge shell-quoted inline prompts.
- Keep logs under `~/.hermes/independent_tasks/logs/` and include the systemd unit name in status replies.
- If final delivery is required, include `messaging` in the toolsets and explicitly instruct the task to send the final deliverable back to the user.
- Before claiming the task survived a gateway restart, verify with `systemctl status hermes-task-NAME` after the restart.
