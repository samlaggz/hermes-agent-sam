# Gateway-independent Magnific background runs

Use this when a long Magnific job must survive Telegram gateway restarts or model changes in the live chat.

## Why
Gateway-bound `terminal(background=true)` processes can be killed when `hermes gateway restart` restarts the gateway service. For multi-hour Magnific runs, launch a separate OS-level service instead.

## Pattern
1. Write a self-contained prompt file for the worker:
   - current project path
   - model/provider requirements
   - skill list
   - exact deliverables
   - capacity/wait retry policy
   - delivery instructions
2. Launch it as a transient systemd service with explicit model/provider:

```bash
systemd-run \
  --unit hermes-task-magnific-v4 \
  --description "Hermes independent Magnific job" \
  --working-directory /tmp/horror_short_project \
  --property Restart=no \
  --property StandardOutput=append:/root/.hermes/independent_tasks/logs/magnific-v4.log \
  --property StandardError=append:/root/.hermes/independent_tasks/logs/magnific-v4.log \
  hermes chat -Q --pass-session-id \
    --source independent:magnific-v4 \
    --provider openai-codex \
    -m gpt-5.5 \
    -s magnific-short-video-production,minimax-hailuo-23-json-prompting \
    -t browser,terminal,file,vision,skills,todo,messaging \
    -q "$(cat /tmp/horror_short_project/magnific_worker_prompt.txt)"
```

3. Give the user both the unit and log path:

```bash
systemctl status hermes-task-magnific-v4 --no-pager
tail -f /root/.hermes/independent_tasks/logs/magnific-v4.log
```

4. If the user changes model/plan:
   - stop obsolete unit: `systemctl stop hermes-task-magnific-v4`
   - start a new unit with a new name and explicit `--provider` / `-m`
   - if useful, resume a prior Hermes session with `--resume SESSION_ID` while changing the model flags

## Notes
- The live chat model and the background job model are independent. Always pin the background job model explicitly.
- Prefer a new unit name for major plan changes so logs remain auditable.
- Do not claim final media was delivered unless the worker output confirms it or the file is verified and sent.
