# Jarvis AI Assistant

Jarvis ist ein KI-gestützter persönlicher Assistent für Windows, der Sprachsteuerung, natürliche Sprachverarbeitung und Aufgabenautomatisierung kombiniert, um alltägliche Aufgaben effizienter und intelligenter zu gestalten.

Das Projekt befindet sich aktuell in aktiver Entwicklung und wird kontinuierlich erweitert.

---

# Support

Falls bei der Installation oder Nutzung von Jarvis Probleme auftreten oder du Fragen hast, stehen dir folgende Möglichkeiten zur Verfügung.

## GitHub Issue

Erstelle ein **Issue** direkt im GitHub-Repository und füge nach Möglichkeit folgende Informationen hinzu:

- Windows-Version
- Python-Version
- Vollständige Fehlermeldung
- Beschreibung des Problems

## Discord

Alternativ kannst du mich auch direkt über Discord kontaktieren.

**Discord:** `Ninjakeks_tvv`

---

# Features

- 🎤 Sprachsteuerung
- 🤖 OpenAI Integration
- 🖥️ Programme öffnen
- ❌ Programme schließen
- 🌐 Webseiten öffnen
- 🎵 Spotify steuern
- ▶️ YouTube Suche
- 📂 Ordner öffnen
- 🔊 Lautstärkesteuerung
- 📋 Automatische Programmerkennung
- ⚡ Automatische Suche nach installierten und portablen Programmen
- 🖥️ Desktop Benutzeroberfläche (UI)

---

# Voraussetzungen

- Windows 10 oder Windows 11
- Python 3.12 oder neuer

---

# Installation

## 1. Repository herunterladen

Repository klonen:

```bash
git clone https://github.com/Ninjakekstvv/Jarvis-AI-Assistant.git
```

oder als ZIP-Datei herunterladen und entpacken.

---

## 2. Virtuelle Umgebung erstellen

```bash
python -m venv .venv
```

---

## 3. Virtuelle Umgebung aktivieren

### Windows CMD

```cmd
.venv\Scripts\activate.bat
```

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

---

## 4. Alle benötigten Bibliotheken installieren

```bash
pip install -r requirements.txt
```

Hierdurch werden automatisch alle benötigten Bibliotheken installiert.

---

## 5. OpenAI API-Key einrichten

Erstelle im Hauptverzeichnis eine Datei mit dem Namen

```
.env
```

und füge Folgendes ein:

```env
OPENAI_API_KEY=DEIN_API_KEY
```

---

## 6. Jarvis starten

Python

```bash
python jarvis.py
```

oder unter Windows

```
start_jarvis.vbs
```

---

# Projektstruktur

```
Jarvis-AI-Assistant
│
├── actions.py
├── ai.py
├── commands.py
├── config.py
├── events.py
├── ipc.py
├── jarvis.py
├── listen.py
├── manifest.py
├── maus.py
├── program_scanner.py
├── programs.py
├── programs_window.py
├── speech.py
├── ui.py
├── voice_state.py
├── requirements.txt
├── start_jarvis.vbs
├── LICENSE
└── README.md
```

---

# Hinweise

- Beim ersten Start werden installierte Programme automatisch erkannt.
- Portable Programme werden ebenfalls erkannt, sofern sie sich auf den angegebenen Laufwerken befinden.
- Einige KI-Funktionen benötigen eine aktive Internetverbindung.
- Für OpenAI-Funktionen wird ein gültiger OpenAI API-Key benötigt.
- Nach dem Erstellen des API-Keys muss dieser mit Guthaben aufgeladen werden (z. B. 5 USD), damit die OpenAI API genutzt werden kann.
- Ohne verfügbares Guthaben kann keine Verbindung zur OpenAI API hergestellt werden. In diesem Fall stehen KI-Funktionen nicht zur Verfügung und Jarvis gibt eine entsprechende Fehlermeldung aus.

---

# Lizenz

Dieses Projekt steht unter der **MIT License**.

Du darfst dieses Projekt:

- ✅ verwenden
- ✅ verändern
- ✅ erweitern
- ✅ veröffentlichen
- ✅ privat oder kommerziell nutzen

Bitte lasse den Copyright-Hinweis und die MIT-Lizenz im Projekt bestehen.

Weitere Informationen findest du in der Datei **LICENSE**.

---

# Version

**Aktuelle Version**

```
v0.1.0 Alpha
```

Dieses Projekt befindet sich derzeit in der **Alpha-Phase**. Fehler können auftreten und Funktionen werden kontinuierlich erweitert.
