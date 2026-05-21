---
name: document-narration-workflows
description: "Extract text from PDFs/documents, clean it for narration, and produce listenable TTS with fallback paths."
version: 1.0.0
author: <REDACTED_PUBLIC_BACKUP>
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [pdf, documents, tts, narration, audio, extraction]
---

# Document Narration Workflows

Use this when the user wants a document turned into spoken audio: extract text, clean it for speech, choose a suitable voice, generate TTS, and return both the text and audio artifacts.

## When to trigger

- User says "extract text from this PDF and make TTS"
- User wants a document narrated for review, social content, or voiceover
- A local PDF must become audio without a full video workflow

## Core workflow

1. **Extract text first**
   - For local PDFs, prefer lightweight text extraction before OCR-heavy tools.
   - If system Python is externally managed, use the Hermes venv instead of forcing global installs.
   - Safe install path:
     ```bash
     /usr/local/lib/hermes-agent/venv/bin/python -m pip install pymupdf
     ```
   - Then extract with the Hermes venv, saving a raw text file.

2. **Read and clean for speech**
   - Remove zero-width characters and awkward line breaks.
   - Collapse wrapped lines into readable sentences.
   - Normalize punctuation that often breaks TTS or sounds unnatural in narration.
   - Save a second cleaned narration file instead of overwriting the raw extraction.

3. **Choose voice based on content**
   - Real-estate, business, and presentation copy usually works best with a calm, polished English voice.
   - Prefer a slightly deeper, confident narration style for luxury/business copy.
   - If you temporarily change Hermes TTS config for a specific voice, restore the prior default after generation.

4. **Generate TTS with verification**
   - Try the normal Hermes `text_to_speech` path first when available.
   - Verify that an actual audio file is produced, not just a claimed success.
   - If the provider fails silently or returns no audio, switch to a working fallback path immediately.

5. **Return both artifacts**
   - Give the user:
     - extracted text
     - audio file
     - file paths if useful
   - Briefly note any fallback used, especially if the default TTS provider did not produce audio.

## Preferred fallback path

When Hermes Edge TTS does not return audio, use `gTTS` inside the Hermes venv instead of repeatedly retrying the same failing tool path.

```bash
/usr/local/lib/hermes-agent/venv/bin/python -m pip install gTTS
```

Then synthesize from the cleaned narration text using a small Python snippet in the Hermes venv.

## Pitfalls

- Do **not** treat raw PDF extraction as narration-ready text.
- Do **not** keep retrying TTS blindly after repeated `No audio was received` style failures; diagnose once, then switch to fallback.
- Do **not** leave the user's global/default Hermes TTS voice changed after a one-off narration task.
- Do **not** overwrite the raw extracted text; keep raw and cleaned outputs separate.

## Output standard

Provide:
- a short confirmation
- the extracted text or a clean excerpt
- a `MEDIA:` audio attachment
- note of any fallback path used

## Reference

See `references/pdf-local-extraction-and-tts-fallback.md` for the concrete local-PDF + Hermes-venv + gTTS fallback recipe proven in-session.
