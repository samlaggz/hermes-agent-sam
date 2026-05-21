# Local PDF extraction + TTS fallback recipe

This reference captures a durable pattern that worked in practice for turning a local PDF into audio on a Hermes host.

## Situation

- Local PDF was provided as a file on disk.
- System Python was externally managed, so `python3 -m pip install ...` failed with the PEP 668 style restriction.
- Hermes default Edge TTS path returned `No audio was received` repeatedly.

## Working extraction path

Use the Hermes venv, not system Python:

```bash
/usr/local/lib/hermes-agent/venv/bin/python -m pip install pymupdf
```

Minimal extraction pattern:

```python
from pathlib import Path
import pymupdf

pdf = Path('/path/to/input.pdf')
out = Path('/tmp/extracted.txt')
doc = pymupdf.open(str(pdf))
text = "\n\n".join(page.get_text("text") for page in doc).strip()
out.write_text(text)
```

## Cleaning pattern for narration

Use a separate cleaned file:

```python
from pathlib import Path
text = Path('/tmp/extracted.txt').read_text()
text = text.replace('\u200b', '')
text = text.replace(' \n', ' ')
text = text.replace('\n', ' ')
while '  ' in text:
    text = text.replace('  ', ' ')
text = text.strip()
Path('/tmp/clean.txt').write_text(text)
```

## Fallback TTS path when Edge returns no audio

Install `gTTS` inside the Hermes venv:

```bash
/usr/local/lib/hermes-agent/venv/bin/python -m pip install gTTS
```

Generate MP3:

```python
from pathlib import Path
from gtts import gTTS

text = Path('/tmp/clean.txt').read_text().strip().rstrip('”"')
out = '/tmp/output.mp3'
gTTS(text=text, lang='en', tld='com', slow=False).save(out)
print(out)
```

## Operational lesson

If Hermes `text_to_speech` fails multiple times with the same Edge no-audio symptom, stop looping and switch to the fallback path after one diagnostic pass.

## Cleanup / courtesy

If you temporarily changed Hermes TTS voice config for the task, restore the previous default afterward so the session does not leave a surprise config change behind.
