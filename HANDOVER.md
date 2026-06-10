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
- **Pentatonische Hintergrundmusik** (C-Dur Pentatonik, sanfte Oszillatoren + Kompressor)
- **Bellen** (`bellen()`): Sägezahn-Oszillator + Bandpass-Filter, 2 Bellen-Impulse
- Bark-Volume bewusst lauter als Musik gesetzt

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

### Bekannte Bugs (unbestätigt behoben)
- Sprachausgabe (`speechSynthesis`) wurde in mehreren Sessions als "still silent" gemeldet
  - Der Safari-Fix (sync vor AudioContext) wurde gepusht, aber die finale Bestätigung vom User steht aus
  - Falls es wieder nicht spricht: `sprechen()` aufrufen → im Browser-Konsole auf Fehler prüfen → sicherstellen, dass `aktuelleAussage` nicht `null` nach `speak()`

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
