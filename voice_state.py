"""Kleiner, prozessübergreifender Statuskanal für die Jarvis-Sprachzustände."""

import json
import os
import sys
import tempfile
import time
from pathlib import Path


STATE_FILE = Path(tempfile.gettempdir()) / "jarvis_voice_state.json"
HEARTBEAT_ENV = "JARVIS_VBS_HEARTBEAT"


def log(message):
    """Konsolenausgabe nur verwenden, wenn Python mit stdout gestartet wurde."""
    if sys.stdout is not None:
        print(message)


def launcher_is_alive(max_age=3.0):
    """Prüft den unsichtbaren VBS-Heartbeat; direkte Python-Starts bleiben erlaubt."""
    heartbeat = os.environ.get(HEARTBEAT_ENV)
    if not heartbeat:
        return True
    try:
        return time.time() - Path(heartbeat).stat().st_mtime <= max_age
    except OSError:
        return False


def set_voice_state(state, message=""):
    """Schreibt den Zustand atomar, damit die UI nie eine halbe JSON-Datei liest."""
    payload = {"state": state, "message": message}
    temporary = STATE_FILE.with_suffix(".tmp")
    try:
        temporary.write_text(json.dumps(payload), encoding="utf-8")
        os.replace(temporary, STATE_FILE)
    except OSError:
        # Die Sprachsteuerung soll auch ohne Statusanzeige weiter funktionieren.
        pass


def get_voice_state():
    try:
        payload = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        return payload.get("state", "idle"), payload.get("message", "")
    except (OSError, ValueError, TypeError):
        return "idle", ""
