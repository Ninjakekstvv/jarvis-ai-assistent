# jarvis-ai-assistent
Jarvis ist ein KI-gestützter persönlicher Assistent, der Sprachsteuerung, natürliche Sprachverarbeitung und Aufgabenautomatisierung kombiniert, um alltägliche Abläufe effizienter und intelligenter zu gestalten

# Jarvis AI Assistant

Jarvis AI Assistant ist ein KI-gestützter Sprachassistent für Windows, der Programme starten und schließen, Webseiten öffnen, Musik steuern und verschiedene Desktop-Aufgaben automatisieren kann.

Das Projekt befindet sich aktuell in aktiver Entwicklung und wird kontinuierlich erweitert.

---

# Features

- 🎤 Sprachsteuerung
- 🤖 OpenAI Integration
- 🖥️ Programme öffnen und schließen
- 🌐 Webseiten öffnen
- 🎵 Spotify steuern
- ▶️ YouTube Suche
- 🔊 Lautstärkesteuerung
- 📂 Ordner öffnen
- 📋 Automatische Programmerkennung
- 🖥️ Desktop UI
- ⚡ Portable Programme werden automatisch erkannt

---

# Requirements

- Windows 10 / Windows 11
- Python 3.12 oder neuer

---

# Installation

## 1. Repository herunterladen

Repository herunterladen oder klonen.

```bash
git clone https://github.com/Ninjakekstvv/Jarvis-AI-Assistant.git
```

oder als ZIP herunterladen und entpacken.

---

## 2. Virtuelle Umgebung erstellen

```bash
python -m venv .venv
```

---

## 3. Virtuelle Umgebung aktivieren

CMD

```cmd
.venv\Scripts\activate.bat
```

PowerShell

```powershell
.venv\Scripts\Activate.bat
```

---

## 4. Alle benötigten Bibliotheken installieren

```bash
pip install -r requirements.txt
```

Dadurch werden automatisch alle benötigten Bibliotheken installiert:

- OpenAI
- Edge-TTS
- SpeechRecognition
- PyAudio
- PySide6
- pygame
- pywhatkit
- requests
- beautifulsoup4
- psutil
- pyautogui
- keyboard
- pywin32
- Pillow
- python-dotenv

---

## 5. OpenAI API-Key eintragen

Im Hauptverzeichnis eine Datei

```
.env
```

erstellen.

Inhalt:

```env
OPENAI_API_KEY=DEIN_API_KEY
```

---

## 6. Jarvis starten

Python

```bash
python jarvis.py
```

oder

per

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
└── README.md
```

---

# Hinweise

- Beim ersten Start werden installierte Programme automatisch erkannt.
- Portable Programme werden ebenfalls erkannt, sofern sie auf den Laufwerken gefunden werden.
- Einige KI-Funktionen benötigen eine aktive Internetverbindung.
- Für OpenAI-Funktionen wird ein gültiger API-Key benötigt.
- Nach dem Erstellen des API-Keys muss dieser mit Guthaben (z. B. 5 USD) aktiviert werden.
- Ohne ausreichendes Guthaben kann keine Verbindung zur OpenAI API hergestellt werden. In diesem Fall gibt Jarvis eine entsprechende Fehlermeldung aus und KI-Funktionen stehen nicht zur Verfügung.

---

# Lizenz

Dieses Projekt befindet sich aktuell in privater Entwicklung.

Eine öffentliche Lizenz wird zu einem späteren Zeitpunkt veröffentlicht.
Dieses Projekt befindet sich aktuell in privater Entwicklung.
