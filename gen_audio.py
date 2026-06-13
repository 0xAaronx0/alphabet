import asyncio, os, sys
import edge_tts

VOICE = "de-DE-AmalaNeural"
RATE = "-12%"
OUT = "audio"

# Ausgeschriebene deutsche Buchstabennamen — verhindert, dass die TTS einzelne
# Buchstaben englisch ausspricht, und macht die Aussprache klar/eindeutig.
# Vokale verlängert (Uuh/Aah), Konsonanten verdoppelt (Ell/Emm/Enn/Err/Ess),
# damit z. B. L klar nach L klingt und U nicht mit O verwechselt wird.
BUCHSTABEN_NAMEN = {
    "a": "Aah", "b": "Beh", "c": "Zeh", "d": "Deh", "e": "Eh",  "f": "Eff",
    "g": "Geh", "h": "Hah", "i": "Ieh", "j": "Jott","k": "Kah", "l": "Ell",
    "m": "Emm", "n": "Enn", "o": "Oh",  "p": "Peh", "q": "Kuh", "r": "Err",
    # "Ix" wuerde als roemische Zahl IX ("neun") gelesen — deshalb "Iks"
    "s": "Ess", "t": "Teh", "u": "Uuh", "v": "Fau", "w": "Weh", "x": "Iks",
    "y": "Ypsilon", "z": "Zett",
}

# Level 2 (Einhorn): kurze Wörter, die buchstabiert werden
WOERTER = ["Haus", "Maus", "Wurm", "Baum"]

entries = {}
for c, name in BUCHSTABEN_NAMEN.items():
    entries[f"finde_{c}"] = f"Finde {name}!"
    entries[f"hoppla_such_{c}"] = f"Hoppla! Such das {name}!"
    entries[f"nein_such_{c}"] = f"Nein! Such das {name}!"
    # Nur der Buchstabe selbst – für das Einhorn-Spiel
    entries[f"nur_{c}"] = f"{name}!"
for n in range(21):
    entries[f"finde_{n}"] = f"Finde {n}!"
    entries[f"hoppla_such_{n}"] = f"Hoppla! Such die {n}!"
    entries[f"nein_such_{n}"] = f"Nein! Such die {n}!"
entries["super"] = "Super!"
entries["super_buchstaben_geschafft_jetzt_kommen_zahlen"] = "Super! Buchstaben geschafft! Jetzt kommen Zahlen!"
entries["wahnsinn_du_hast_alle_zahlen_gefunden"] = "Wahnsinn! Du hast alle Zahlen gefunden!"
entries["wahnsinn_du_hast_alle_buchstaben_gefangen"] = "Wahnsinn! Du hast alle Buchstaben gefangen!"
entries["schade_versuch_es_nochmal"] = "Schade! Versuch es nochmal!"
# Level 2 (Einhorn): Wort-Ansagen + Übergänge
for w in WOERTER:
    entries[f"wort_{w.lower()}"] = f"{w}!"
entries["super_jetzt_kommen_woerter"] = "Super! Jetzt suchen wir Wörter!"
entries["wahnsinn_du_hast_alle_woerter_geschafft"] = "Wahnsinn! Du hast alle Wörter geschafft!"

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
