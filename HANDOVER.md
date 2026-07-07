# Projekt-Handover: Alphabet-Lernspiele für Kinder

## Kontext

Der User (aaron@nabla.fi) baut Browser-Lernspiele für seine **5-jährige Tochter**, die dabei hilft, Buchstaben und Zahlen auf Deutsch zu lernen. Alle Spiele sind **Single-File HTML** (kein Framework, kein Build-Step, keine externen Assets).

**Repo:** `0xAaronx0/alphabet`  
**Branch:** `claude/jump-run-game-30bc9`  
**Lokales Verzeichnis:** `/home/user/alphabet/`  
**Git-Remote (lokaler Proxy):** `http://local_proxy@127.0.0.1:*/git/0xAaronx0/alphabet`

---

## Spiele

### 1. `index.html` — Buchstaben Fang! (Jump-Run)
- Marshall (PAW Patrol Dalmatiner mit rotem Feuerwehr-Helm "03" und Knochen-Abzeichen) läuft am Boden
- Buchstaben/Zahlen fallen von oben, Spieler springt mit **Leertaste oder Pfeil-hoch**
- **Level 1:** 26 Buchstaben (A–Z), muss 15 fangen → Level-Übergang
- **Level 2:** Zahlen 0–20, muss 15 finden → Gewonnen
- Keyboard-Controls → wurde als **zu schwer für 5-Jährige** befunden → deshalb `blasen.html`
- Hintergrund Level 1: Taghimmel; Level 2: Sonnenuntergang

### 2. `blasen.html` — Buchstaben-Blasen! (Click/Tap) ← **Haupt-Spiel**
- Seifenblasen mit Buchstaben steigen von unten auf, Kind **tippt/klickt** die richtige Blase
- Keine Tastatur, kein Game-Over, keine Leben — nur positive Verstärkung
- Falsches Tippen: Blase wackelt, Stimme sagt "Hoppla! Such a!" (nicht bestrafend)
- Richtiges Tippen: Pop-Sound, Konfetti, Marshall-Freudenhüpfer + Bellen, "Super!"
- **Level 1:** 15 Buchstaben → Level 2: 15 Zahlen (0–20)
- HUD: `🦴 X / 15`
- **Ziel-Auswahl (seit 2026-06-13):** Das Ziel ist ZUFÄLLIG eine der bereits sichtbaren Blasen
  (`zielAusBlasen()`), nicht mehr die frisch gespawnte → vorher zu leicht. Blasen spawnen variierte,
  doublettenfreie Zeichen (`naechstesFreiesZeichen()`); nach jedem Treffer / wenn das Ziel
  ungetippt nach oben rausschwebt wird neu gewählt (`zielLeeren()` → `zielPending`). Erstes Ziel +
  ein paar Startblasen werden in `spielStart()` synchron gesetzt (Safari: Ansage VOR `musikStarten`).

### 3. `einhorn.html` — Einhorn-Buchstaben! (Endless-Runner, seit 2026-06-13)
Im Stil von „Robot Unicorn Attack": ein Einhorn rennt mit konstanter Geschwindigkeit durch eine
Fantasy-Welt (Parallax: Regenbogen, Sterne, driftende Wolken, Parallax-Hügel, Lauf-Streifen am
Boden). Oben fliegen Buchstabenblasen von rechts herein. **Pfeil hoch / Leertaste / Tippen = Hüpfen**
(Doppelsprung erlaubt); das Einhorn zerplatzt mit dem **Horn** die Zielblase. Angesagt wird **nur der
Buchstabe** (z. B. „Zett") über `audio/nur_<x>.mp3` (`buchstabeAnsagen`→`clipAnsage`).
Auf dem Server `einhorn.html`.

**Drei Level (10/3/10 seit 2026-06-20; gilt genauso für `biene.html`):**
- **Level 1** (`level===1`): 10 einzelne Buchstaben fangen (`ZIEL_PRO_LEVEL=10`)
  → `zustand='levelzwischen'` (Übergangs-Screen) → `level2Starten()`.
- **Level 2** (`level===2`): 3 kurze Wörter buchstabieren. **Vorrat `WORT_VORRAT` = 18 Wörter** mit
  Emoji (nur A–Z, keine Umlaute/ß – sonst fehlt der Buchstaben-Clip). Pro Spiel wählt `woerterWaehlen()`
  3 davon → `WOERTER` (in `spielStart` gesetzt); **höchstens 2 wie im vorigen Spiel** (`letzteWoerter`).
  Jedes Wort braucht `audio/wort_<wort>.mp3` (alle 18 via `gen_audio.py` erzeugt). Beim Erweitern des
  Vorrats: Wort-Clip mit erzeugen.
  Jedes Wort startet mit `wortStarten()`: sagt ZUERST das ganze Wort an (`wort_<x>.mp3`), dann (über
  `ansageTimer`≈90) den ersten Buchstaben. `naechstesZiel()` liefert den nächsten fehlenden Buchstaben;
  gefangene Buchstaben sammeln sich in `gebaut` und werden oben links als Wort-Baukasten gezeigt
  (Bild + Buchstaben + `_`-Slots, `anzeigeZeichnen`). Wort komplett → `wortFertigPending`, nach dem
  Jubel (`update`) nächstes Wort (wieder Wort-zuerst) bzw. nach 3 Wörtern → `zustand='levelzwischen2'`.
- **Level 3** (`level===3`, seit 2026-06-20): **Englische Begriffe.** Vorrat `ENGLISCH_VORRAT` =
  24 Wort+Emoji-Paare (hand ✋, ear 👂, house 🏠 …; OHNE bee/tree — Biene/Bäume sind im Spiel
  Deko bzw. Spielfigur, das angesagte Wort hätte sonst mehrere Bilder). `spielStart()` mischt und
  nimmt `ZIEL_PRO_LEVEL3=15` davon → `ENGLISCH` (Ziel-Reihenfolge; `punkte` ist zugleich der
  Index; schon in spielStart, damit der Zwischenscreen die ECHTEN ersten 4 Bilder zeigen kann).
  Das Wort wird auf ENGLISCH angesagt (`audio/englisch_<wort>.mp3`, en-US-Jenny; `book`/`moon`
  via en-GB-Sonia — Whisper-verifiziert), die Blasen zeigen Emoji-BILDER (`zeichenPool()` liefert
  in Level 3 die Emoji statt `ALPHABET`), gefangen wird das passende Bild.
  Zwischen-Ansage: `toll_jetzt_auf_englisch.mp3`. Kein `superSprechen()` pro Fang (nur
  Jubel-Flash/Konfetti), Ansage-Wiederholung via `zielAnsagen()`.
- **Bonus-Level** (seit 2026-07-07): Nach den 15 englischen Begriffen kommt AUTOMATISCH (ohne
  Klick-Screen) noch einmal die Wort-Mechanik: `fangen` setzt `ziel=null` + `bonusTimer=
  BONUS_ANSAGE_FRAMES` (470 ≈ 7,8 s, damit `bonus_level_ansage.mp3` [7,66 s] ausreden kann),
  `update()` zählt runter und ruft `bonusStarten()`: `bonusRunde=true`, `level=2` (identische
  Wort-Logik!), `BONUS_WOERTER=5` NEUE Wörter (aus `WORT_VORRAT` OHNE die 3 aus Level 2,
  werden an `letzteWoerter` angehängt). HUD zeigt 🎁 statt 📖. Nach 5 Wörtern → `gewonnen`
  (`wahnsinn_du_hast_alle_woerter_geschafft.mp3`); der Gewinn-Screen zeigt die 5 Bonus-Bilder.
  Der Wort-fertig-Zweig in `update()` verzweigt auf `bonusRunde` (gewonnen vs. levelzwischen2).
- **Der gesuchte Buchstabe wird NICHT angezeigt** (nur gesprochen): die Mitte-Pill zeigt „🔊 Hör gut zu!".
  In Level 2 zeigt der Wort-Baukasten oben links nur die schon GEFANGENEN Buchstaben (+ `_`-Slots).
- **Goldener Glow (`glowAktiv()`):** Level 1 nur die ersten 6 Treffer (`punkte<6`); Level 2 nur beim
  ersten Wort (`wortIndex===0`); Level 3 die ersten 8 Begriffe (`punkte<8`). Danach muss das Kind
  die richtige Blase selbst finden. `glowAktiv()` steuert `leuchtet` in `blaseErzeugen` UND `zielMarkieren`.

Schlüssel-Details:
- Auf den Boden gebaut wie die anderen, aber Spieler hat `sy/vy` (Sprung), Welt scrollt über `weltX`.
- **Horn-Kollision:** `spielerZeichnen()` schreibt die Welt-Position der Hornspitze via
  `ctx.getTransform()` nach `hornWelt`; `update()` prüft Abstand `hornWelt`↔Blase (nur Zielblase
  ist fangbar; falsche wackeln nur). `update` läuft vor `zeichnen`, nutzt also `hornWelt` vom Vorframe.
- **Kein Ketten-Treffer:** Kollision pausiert solange `flashTimer>0` (Jubel ~1 s nach Fang),
  sonst würde ein Sprung mehrere Buchstaben auf einmal fangen.
- Reichweite hängt an Geometrie: `BAND_MITTE`/`BAND_STREU` (Flughöhe) + `FANG_R` (Fang-Radius)
  vs. Stand-Hornhöhe. **Invariante:** Stand-Horn muss > `FANG_R` über der untersten Blase liegen,
  sonst Treffer OHNE Sprung; und der Sprung-Apex muss bis ins Band reichen. **Beim Ändern der
  Einhorn-Größe** Stand-`hornWelt.y` neu messen (Spiel starten, `hornWelt.y` bei `sy==0` lesen) und
  `BAND_MITTE` anpassen. Aktuell: Stand-Horn ≈ GROUND−150, `BAND_MITTE`=GROUND−262, `FANG_R`=BLASE_R+22.
- Das Einhorn ist im **niedlichen Chibi-Stil** gezeichnet (`spielerZeichnen`: großer Kopf, großes
  glänzendes Auge, rosa Wange, fluffige Regenbogen-Mähne+Schweif, Spiralhorn, Stummelbeine mit
  rosa Hufen). **Sticker-Umriss-Trick:** `silhouette()` zeichnet alle weißen Teile zuerst dunkel
  (etwas größer) und dann weiß → sauberer Cartoon-Umriss ohne innere Linien.
- **rAF pausiert im Headless-Preview** → Gameplay deterministisch testen: `update()`+`spielerZeichnen()`
  pro Frame manuell in einer Schleife aufrufen (hält `hornWelt` aktuell), nicht per Auto-Klick/Timer.
- `funkeln()` (magischer Klang) statt `bellen()` (Hund) beim Fangen.
- **Deko (rein kosmetisch, `DEKO_ALPHA`=0.9, 3 Parallax-Ebenen seit 2026-06-14):** `hillDeko`
  (Schloss/Baum/Regenbogen, sitzt via `huegelObenNah(x)` AUF den Hügeln, Hügel-Tempo), `midDeko`
  (Bäume/Bodentiere am Boden, `MID_V=WELT_V*0.6`) und `flieger`. Alle Emoji werden als
  **Offscreen-Sprites** vorgerendert und per `drawImage` geblittet (`dekoSprite()`) —
  `fillText(Emoji)+globalAlpha` rendert in Chrome blass, NICHT zurückbauen. `flieger` (je mit
  `typ`: 'w'=Schmetterling/Fee horizontaler Flügelschlag, 's'=Vogel/Biene), selten (~14–28 s), fliegen
  nach rechts-oben und werden in `fliegerZeichnen` **gespiegelt** (`scale(-…,…)`) → Kopf voraus in
  Flugrichtung; 's'-Typen nur vertikal pulsieren (sonst staucht der horizontale Schlag sie zum „Kopf").
  Anzahl bewusst gering (User-Wunsch).

### 4. `biene.html` — Bienen-Buchstaben! (seit 2026-06-20)
Variante von `einhorn.html` (Kopie, dann umgebaut): statt rennendem Einhorn **fliegt eine Biene**
(im Canvas gezeichnet: gelb gestreifter Körper, große Augen, Fühler, Stachel, schlagende Flügel,
kippt mit `spieler.tilt` in Flugrichtung). **Pfeil hoch/runter HALTEN = höher/tiefer fliegen**
(`steuerUp`/`steuerDown` via keydown/keyup, keine Schwerkraft); **Touch: Biene folgt der
Finger-Höhe** (`zeigerAktiv`/`zeigerY`, pointerdown/move). Flughöhe `spieler.byY` geklemmt auf
`FLY_TOP=130`…`FLY_BOTTOM=GROUND−30`, `FLY_SPEED=5` mit Glättung. Fang = Bienenkörper (`UX`,
`spieler.byY`) überlappt Zielblase (`FANG_R=BLASE_R+26`, kein Horn/`hornWelt`). Blasen spawnen über
die ganze Flughöhe statt im Band. Alles andere (Audio, Musik, Deko-Sprites, Parallaxe, die drei
Level inkl. Englisch, Glow-Regeln, Fixed-Timestep) ist identisch mit `einhorn.html` — **Level-Logik-
Änderungen immer in BEIDEN Dateien machen** (die Blöcke sind textidentisch, ein gemeinsames
Python-Transform-Skript pro Änderung hat sich bewährt). Menü-Kachel (honiggelb) in `start.html`.

### Design (alle Spiele, seit 2026-06-13)
Modernes Kinder-Browsergame-Layout statt 90er-Look: weiche Pastell-Landschaft (driftende Wolken,
Sonne mit Halo, runde Hügel), runde Schrift (`SCHRIFT`-Konstante), flache Blasen/Buchstaben mit
weichem Schlagschatten, weiße Glas-Pills im HUD, Karten-Screens (`karteZeichnen`/`knopfZeichnen`)
mit pinken Gradient-Buttons, Konfetti (Kreise + rotierende Streifen). Startseite = `start.html`
(im Repo, 3 Buttons), auf dem Server als `index.html` deployt. `einhorn.html` ist aus `blasen.html`
abgeleitet → **Audiosystem/Groove-Musik/Helfer sind identisch**, nur die Spiel-Logik unterscheidet sich.

---

## Technische Details

### Canvas / Rendering
- Canvas: 800×600, CSS-skaliert (`Math.min(innerWidth/W, innerHeight/H) * 0.97`)
- `pointerdown` für Click+Touch (kein separates `touchstart`)
- Koordinatenmapping: `(e.clientX - rect.left) / scaleX`

### Web Speech API (KRITISCH — Safari-Bugs!)
```javascript
let aktuelleAussage = null; // WICHTIG: verhindert GC der Utterance

function sprechen(text, tempo = 0.82, tonhöhe = 1.25) {
    synth.cancel();
    aktuelleAussage = sprechEinheit(text, tempo, tonhöhe);
    synth.speak(aktuelleAussage);
}
```

**Safari-Fix (unveränderlich wichtig):**
- `buchstabeAnsagen(ziel)` muss **synchron und VOR `musikStarten()`** aufgerufen werden
- Safari blockiert `speechSynthesis.speak()` nach `AudioContext`-Erstellung
- **KEIN `setTimeout`** zwischen `cancel()` und `speak()` — das bricht Safari, weil der User-Gesture-Kontext verloren geht
- Deutsche Stimme: Priorität "Anna", Fallback erste `de`-Stimme, dann `onvoiceschanged`

### Web Audio API
- `AudioContext` wird beim ersten User-Interaktion erstellt (Browser-Policy)
- **Hintergrundmusik seit 2026-06-13: leiser, eigener Baile-Funk-Groove** (Drum-Machine aus
  Oszillatoren + Rauschen): `KICK`/`CLAP`/`HAT`/`BASS_WURZEL`/`MELODIE`-Pattern (16tel, 4-Takt-Loop,
  128 BPM) → `grooveSchedulieren()` mit `kick/clap/hat/bass/pluck`. Lautstärke zentral über
  `MUSIK_LAUTSTAERKE` (0.06) am `masterGain`. **Wichtig:** ist eine EIGENE Komposition im Stil von
  „No Batidão" — NICHT das Originalstück (Urheberrecht; das echte Lied darf nicht nachgebaut/
  eingebettet werden, auch nicht privat). Wollte der User das echte Stück, müsste er selbst eine
  Datei bereitstellen, die ihm gehört. Vorgänger: dezente „Spieluhr" (54 BPM), davor Melodie+Bass+
  Akkorde (war zu aufdringlich).
- **Bellen** (`bellen()`) + **Plopp** (`ploppen()`): hängen direkt an `audioCtx.destination` (NICHT
  am `masterGain`) → bleiben in voller Lautstärke, unabhängig von der leisen Musik. Bark bewusst laut.
- **Blasen-Optik (2026-06-11):** Der weiße **Lichtreflex** (Glanz-Verlauf + Glanzpunkt-Ellipse) auf
  den Blasen lag teils über dem Buchstaben → entfernt, Füllung jetzt dezenter Farbverlauf ohne Weiß.
  Der **goldene Ziel-Glow** (GLOW_UNTIL, erste 6 Runden) ist bewusst DRIN — der User wollte ihn
  behalten (kurzzeitig fälschlich entfernt, weil "Glow" missverstanden wurde)

### Marshall-Charakter (in beiden Spielen identisch)
- Dalmatiner: weiß/schwarz-gefleckt, runder Kopf mit Schnauze
- Rotes Feuerwehr-Helm mit Aufschrift "03"
- Knochen-Abzeichen auf der Brust
- Floppy Bézier-Ohren
- In `blasen.html`: macht Freudenhüpfer bei richtigem Tipp

---

## Letzter Stand / Offene Aufgaben

### Zuletzt committed (c12781a)
`blasen.html` wurde erstellt und gepusht. Beide Spiele sind funktionsfähig.

### ✅ ERLEDIGT (2026-06-10): VPS-Hosting — Spiele sind live

**https://abc.kitescout.tech** — Startseite mit zwei großen Buttons:
- `/blasen.html` — Buchstaben-Blasen (Haupt-Spiel)
- `/fang.html` — Buchstaben Fang (= `index.html` aus dem Repo, auf dem Server umbenannt)
- `/` — neue kindgerechte Startseite (liegt nur auf dem Server, nicht im Repo)

Setup (gleiches Muster wie `cruise-map`/`nabla-dashboard` auf dem KiteScout-VPS):
- Hostinger-VPS `1601314` (`187.77.70.112`), Dateien unter `/docker/alphabet/html/`
- Docker-Projekt `alphabet`: `nginx:alpine` + Traefik-Labels `Host(abc.kitescout.tech)`, websecure + letsencrypt
- DNS: A-Record `abc.kitescout.tech` → `187.77.70.112` (TTL 300)
- SSH vom Mac: `ssh -i ~/.ssh/hostinger_vps root@187.77.70.112` (IPv6-Alias `hostinger` geht nur in Netzen mit IPv6)
- Spiel-Update deployen: neue Datei per `scp` nach `/docker/alphabet/html/` — kein Container-Neustart nötig

### ✅ Sprachausgabe (Stand 2026-06-10)
- User bestätigt: Sprachausgabe **funktioniert** — aber die Systemstimme klang unangenehm
- Deshalb umgestellt auf **vorab erzeugte MP3-Clips** (Microsoft `de-DE-AmalaNeural` via edge-tts, Rate −12%; vorher Katja — User fand sie unangenehm):
  - `audio/` — 145 Clips (finde_X, hoppla_such_X, nein_such_X für a–z + 0–20, plus 4 Festsätze)
  - `gen_audio.py` erzeugt sie neu: `uv run --with edge-tts python gen_audio.py`
  - **Buchstaben werden ausgeschrieben** in `BUCHSTABEN_NAMEN` — einzelne Großbuchstaben las die
    TTS teils englisch ("find i"); ACHTUNG: "Ix" wird als römische Zahl IX ("neun") gelesen → "Iks"!
    Aussprache mehrfach geschärft. Erkenntnisse (per Whisper-Vergleich über mehrere Stimmen, da man
    Einzel-Clips nicht zuverlässig automatisch prüfen kann — Methode: Kandidaten erzeugen, mit
    `faster-whisper` language="de" transkribieren, klarste Schreibweise/Stimme wählen):
    • **L:** Amala spricht L undeutlich (klingt wie „Ja") → `VOICE_OVERRIDE = {"l": Katja}` (Katja sagt klar „El").
    • **J:** „Jott" klingt wie „Tschüss" → `"Jot"` (klar).
    • **U:** „Uuh"/„Uh" klingt wie „O" → `"Uu"` (klar als U).
    • Sonst: Vokale verlängert (A="Aah"), Konsonanten verdoppelt (M/N/R/S/Ell). `VOICE_OVERRIDE` erlaubt
      pro Buchstabe eine andere Stimme. Beim Ändern betroffene Clips löschen + neu erzeugen.
  - **Level-2-Clips:** `wort_<wort>.mp3` für alle 18 `WORT_VORRAT`-Wörter + `super_jetzt_kommen_woerter`.
  - **Level-3-/Bonus-Clips:** `englisch_<wort>.mp3` für alle 24 Pool-Wörter (en-US-Jenny;
    `book`/`moon` en-GB-Sonia) + `toll_jetzt_auf_englisch` + `bonus_level_ansage` (Übergang ins
    Bonus-Level) + `wahnsinn_du_hast_alle_woerter_geschafft` (Sieg nach dem Bonus).
    Insgesamt 219 Clips im Ordner (2 davon verwaist: `wahnsinn_du_hast_alle_buchstaben_gefangen`,
    `wahnsinn_du_kannst_schon_englisch`).
  - **Hinweis:** Aussprache kann nur der Mensch final beurteilen (Whisper hört Einzel-Clips falsch) —
    bei Beschwerden gezielt die `BUCHSTABEN_NAMEN`-Schreibweise des Buchstabens anpassen.
  - Sprach-Check: `uv run --with faster-whisper python check_audio.py` (Whisper-Transkription;
    Sprach-Erkennung bei 2-s-Clips notorisch unzuverlässig — im Zweifel mit language="de" forcieren
    und Transkript lesen; identische md5-Hashes zweier Clips = falsch normalisierter Text)
  - `sprechen()` spielt jetzt den passenden Clip über EIN wiederverwendetes `Audio`-Element
    (iOS entsperrt es bei der ersten Geste); Dateiname = `audioSchluessel(text)` (Slug des gesprochenen Texts)
  - **Web Speech bleibt als Fallback** — der alte Safari-Fix (sync vor AudioContext, kein setTimeout) gilt dort weiterhin
- Neue Ansage hinzufügen: Satz in `gen_audio.py` UND im Spiel-Code ergänzen — Slug-Regeln müssen übereinstimmen, sonst greift nur der Fallback

---

## Workflow für neue Session

```bash
# In /home/user/alphabet — Branch prüfen
git status
git log --oneline -5

# Dateien liegen lokal:
# /home/user/alphabet/index.html
# /home/user/alphabet/blasen.html

# Push (falls nötig):
git push -u origin claude/jump-run-game-30bc9
```

### MCP-Zugang prüfen
```bash
# Hostinger MCP sollte in Settings konfiguriert sein
cat ~/.claude/settings.json | grep -i hostinger
# oder
ls ~/.claude/
```

---

## User-Präferenzen
- Kommuniziert auf **Deutsch** (technische Antworten auch Deutsch bevorzugt)
- Möchte Befehle **direkt ausgeführt** haben, nicht nur erklärt bekommen
- Sehr wenig technisches Vorwissen — keine langen Erklärungen
- Priorität: **es funktioniert für das Kind**, nicht technische Perfektion
