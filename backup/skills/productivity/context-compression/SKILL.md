---
name: context-compression
description: Proactive context compression using Honcho — save key facts as conclusions to keep the injected context compact even in marathon sessions. Use when the conversation grows long, before the model starts forgetting, or when the user asks to "compress context."
version: 1.0.0
---

# Context Compression

## Problem

Long conversations inflate the system prompt (messages + tool results + memory injection). Models have fixed context windows (deepseek-v4-pro: 128K tokens). Once exceeded, the oldest content is silently truncated — the model "forgets" early parts of the conversation.

Honcho's base context injection (summary + representation + peer card) also grows over time unless capped.

## Solution: Three-Layer Defense

### Layer 1 — Honcho `contextTokens` Budget (always on)

The `contextTokens` cap in `honcho.json` limits the Honcho-injected context block. When the summary + representation + card exceed this budget, Honcho trims the summary first, then the representation, preserving the card.

```bash
hermes honcho tokens --context 8000    # cap injection at 8000 tokens
```

### Layer 2 — Dialectic Cadence (always on)

`dialecticCadence` controls how often the expensive dialectic LLM fires. Default is 2 (every other turn). Bump to 5 for long sessions.

```bash
# Set in honcho.json hosts block:
"dialecticCadence": 5
```

### Layer 3 — Proactive Compression via `honcho_conclude` (manual)

This is the active compression mechanism. When the conversation is getting long, distill the important parts into conclusions:

```
honcho_conclude conclusion="<specific, durable fact>"
```

**What to save (fits in 8K token budget):**
- User preferences and corrections
- Key decisions made this session
- Project conventions discovered
- Critical context for continuing work

**What NOT to save (stays in session_history/search):**
- Task progress / TODO state
- Transient error messages
- File paths that change
- Anything stale in < 7 days

## When to Compress

| Trigger | Action |
|---------|--------|
| Session > 15 turns | Review session, save 3-5 key facts as conclusions |
| User corrects you | Save the correction immediately |
| Major decision made | Save it as a conclusion |
| Switching tasks within session | Compress current context before starting new task |
| User asks "remember this" | Save it |
| Model starts forgetting early context | Compress aggressively |

## Verification

```bash
hermes honcho status     # check contextTokens budget
hermes honcho tokens     # verify settings
honcho_profile           # see what's in the user card
honcho_context           # full snapshot of what Honcho sees
```

## Config Reference

| Setting | Recommended | Purpose |
|---------|------------|---------|
| `contextTokens` | 8000 | Cap on injected context block |
| `dialecticCadence` | 5 | Turns between dialectic LLM calls |
| `contextCadence` | 1 | Turns between context API calls |
| `recallMode` | `hybrid` | Auto-inject + tools available |
