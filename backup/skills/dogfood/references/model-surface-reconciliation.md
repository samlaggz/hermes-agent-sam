# Model / feature surface reconciliation

Use this when a user asks whether a model, feature, or release is "on the site" or "available now" and the product has multiple surfaces (marketing pages, release posts, in-product picker, API docs, SEO metadata).

## Why

Web products often expose release information unevenly:
- marketing/home pages announce a launch first
- in-product pickers lag behind or roll out gradually
- raw HTML / meta keywords may contain stale, SEO-only, or prelaunch strings

If you check only one surface, you can overstate availability.

## Procedure

1. Check the visible marketing or research surface for announcements.
2. Check the actual product UI where the thing would be used (model picker, settings, dashboard, pricing page, API console).
3. If needed, inspect raw page HTML for exact strings.
4. Classify every finding by confidence:
   - **Visible selectable UI**: highest confidence for user-available access
   - **Visible announcement / release card**: confirms launch messaging, not necessarily rollout
   - **Raw HTML / SEO metadata only**: lowest confidence; treat as supporting evidence only
5. Report the discrepancy plainly: announced vs selectable vs HTML-only mention.

## Example: qwen.ai / Qwen3.7-Max

Observed pattern:
- Homepage research card announced **Qwen3.7: The Agent Frontier** and the visible snippet said **Qwen3.7-Max**.
- Public Qwen Studio model picker still showed **Qwen3.6-Plus**, **Qwen3.6-Max-Preview**, and **Qwen3.6-27B**.
- Raw homepage HTML contained older model-name strings such as **qwen3.5-max-preview** and **qwen3.6-max**, but no exact **qwen3.7-max-preview** string.

Safe conclusion shape:
- **Qwen3.7-Max is announced on qwen.ai**.
- **Qwen3.7-Max-Preview was not visibly selectable in the public Studio picker at the time of inspection**.
- **Do not infer public availability from HTML keywords alone.**
