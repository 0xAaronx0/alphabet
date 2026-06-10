import asyncio, os, sys
import edge_tts

VOICE = "de-DE-KatjaNeural"
RATE = "-12%"
OUT = "audio"

entries = {}
for c in "abcdefghijklmnopqrstuvwxyz":
    entries[f"finde_{c}"] = f"Finde {c.upper()}!"
    entries[f"hoppla_such_{c}"] = f"Hoppla! Such das {c.upper()}!"
    entries[f"nein_such_{c}"] = f"Nein! Such das {c.upper()}!"
for n in range(21):
    entries[f"finde_{n}"] = f"Finde {n}!"
    entries[f"hoppla_such_{n}"] = f"Hoppla! Such die {n}!"
    entries[f"nein_such_{n}"] = f"Nein! Such die {n}!"
entries["super"] = "Super!"
entries["super_buchstaben_geschafft_jetzt_kommen_zahlen"] = "Super! Buchstaben geschafft! Jetzt kommen Zahlen!"
entries["wahnsinn_du_hast_alle_zahlen_gefunden"] = "Wahnsinn! Du hast alle Zahlen gefunden!"
entries["schade_versuch_es_nochmal"] = "Schade! Versuch es nochmal!"

os.makedirs(OUT, exist_ok=True)
sem = asyncio.Semaphore(6)

async def gen(key, text):
    path = os.path.join(OUT, key + ".mp3")
    if os.path.exists(path) and os.path.getsize(path) > 1000:
        return
    async with sem:
        for attempt in range(3):
            try:
                await edge_tts.Communicate(text, VOICE, rate=RATE).save(path)
                if os.path.getsize(path) > 1000:
                    return
            except Exception as e:
                await asyncio.sleep(2 * (attempt + 1))
        print(f"FEHLER: {key}", file=sys.stderr)

async def main():
    await asyncio.gather(*(gen(k, t) for k, t in entries.items()))
    print(f"{len(os.listdir(OUT))} / {len(entries)} Clips erzeugt")

asyncio.run(main())
