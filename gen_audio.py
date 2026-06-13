import asyncio, os, sys
import edge_tts

VOICE = "de-DE-AmalaNeural"
# Manche Buchstaben klingen mit Amala unklar → klarere Stimme pro Buchstabe.
# (per Whisper-Vergleich über mehrere Stimmen ermittelt)
#  L: Amala klingt wie „Ja" → Katja sagt klar „El".
#  U: Amala klingt wie „O" bzw. „o-u" → Seraphina sagt klar „U".
VOICE_OVERRIDE = {
    "l": "de-DE-KatjaNeural",
    "u": "de-DE-SeraphinaMultilingualNeural",
}
RATE = "-12%"
OUT = "audio"

# Ausgeschriebene deutsche Buchstabennamen — verhindert, dass die TTS einzelne
# Buchstaben englisch ausspricht, und macht die Aussprache klar/eindeutig.
# Vokale verlängert (Uuh/Aah), Konsonanten verdoppelt (Ell/Emm/Enn/Err/Ess),
# damit z. B. L klar nach L klingt und U nicht mit O verwechselt wird.
BUCHSTABEN_NAMEN = {
    "a": "Aah", "b": "Beh", "c": "Zeh", "d": "Deh", "e": "Eh",  "f": "Eff",
    "g": "Geh", "h": "Hah", "i": "Ieh", "j": "Jot", "k": "Kah", "l": "Ell",
    "m": "Emm", "n": "Enn", "o": "Oh",  "p": "Peh", "q": "Kuh", "r": "Err",
    # "Ix" wuerde als roemische Zahl IX ("neun") gelesen — deshalb "Iks";
    # "Jott" wird teils als "Tschüss/Tschööt" gelesen → "Jot" (klar als "Jot")
    "s": "Ess", "t": "Teh", "u": "U",   "v": "Fau", "w": "Weh", "x": "Iks",
    "y": "Ypsilon", "z": "Zett",
}

# Level 2 (Einhorn): Vorrat kurzer Wörter, die buchstabiert werden
WOERTER = ["Haus", "Maus", "Wurm", "Baum", "Ball", "Auto", "Hund", "Katze",
           "Sonne", "Mond", "Stern", "Blume", "Apfel", "Fisch", "Herz",
           "Boot", "Ente", "Krone"]

entries = {}
entry_voice = {}   # key -> Stimme (Standard: VOICE)
for c, name in BUCHSTABEN_NAMEN.items():
    keys = [f"finde_{c}", f"hoppla_such_{c}", f"nein_such_{c}", f"nur_{c}"]
    entries[keys[0]] = f"Finde {name}!"
    entries[keys[1]] = f"Hoppla! Such das {name}!"
    entries[keys[2]] = f"Nein! Such das {name}!"
    entries[keys[3]] = f"{name}!"   # nur der Buchstabe – fürs Einhorn-Spiel
    if c in VOICE_OVERRIDE:
        for k in keys: entry_voice[k] = VOICE_OVERRIDE[c]
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
    voice = entry_voice.get(key, VOICE)
    async with sem:
        for attempt in range(3):
            try:
                await edge_tts.Communicate(text, voice, rate=RATE).save(path)
                if os.path.getsize(path) > 1000:
                    return
            except Exception as e:
                await asyncio.sleep(2 * (attempt + 1))
        print(f"FEHLER: {key}", file=sys.stderr)

async def main():
    await asyncio.gather(*(gen(k, t) for k, t in entries.items()))
    print(f"{len(os.listdir(OUT))} / {len(entries)} Clips erzeugt")

asyncio.run(main())
