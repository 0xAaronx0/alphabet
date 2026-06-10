import os, sys
from faster_whisper import WhisperModel

model = WhisperModel("base", device="cpu", compute_type="int8")

probleme = []
dateien = sorted(os.listdir("audio"))
for i, f in enumerate(dateien):
    segments, info = model.transcribe(os.path.join("audio", f), beam_size=3)
    text = " ".join(s.text for s in segments).strip()
    sprache = info.language
    verdaechtig = sprache != "de" or text.lower().startswith("find ") or " find " in text.lower()
    if verdaechtig:
        probleme.append((f, sprache, round(info.language_probability, 2), text))
    if (i + 1) % 30 == 0:
        print(f"  {i+1}/{len(dateien)} geprueft...", flush=True)

print(f"\n{len(dateien)} Clips geprueft, {len(probleme)} verdaechtig:")
for f, sp, p, t in probleme:
    print(f"  {f}: [{sp} {p}] {t!r}")
