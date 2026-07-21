"""Sprachsteuerung mit Wake-Word: Jarvis reagiert erst auf „Jarvis“."""

import datetime
import os
import random
import re
import subprocess
import sys
import threading
import time
import webbrowser

import pywhatkit

from actions import open_program, open_website
from commands import execute_command
from ai import frage_ki
from listen import zuhoeren
from speech import sprechen
from voice_state import launcher_is_alive, log, set_voice_state


antworten_rechner = [
    "Jawohl, Master. Ich öffne den Rechner.",
    "Natürlich, Master. Ich öffne den Rechner.",
    "Der Rechner wird jetzt geöffnet, Master.",
    "Einen Moment bitte, Master. Ich öffne den Rechner.",
    "Sofort, Master. Ich öffne den Rechner.",
]


def starte_ui():
    """Startet das Qt-Fenster mit demselben Python ohne weitere Konsole."""
    ui_path = os.path.join(os.path.dirname(__file__), "ui.py")
    subprocess.Popen([sys.executable, ui_path], close_fds=True)


def supervisor_watchdog():
    """Beendet den Sprachprozess, wenn der aufrufende VBS geschlossen wurde."""
    while True:
        if not launcher_is_alive():
            os._exit(0)
        time.sleep(1)


def ohne_wake_word(text):
    """Entfernt „Jarvis“ aus einem Satz, damit Direktbefehle möglich sind."""
    return re.sub(r"\bjarvis\b", "", text, flags=re.IGNORECASE).strip()


def youtube_abspielen(suche):
    sprechen(f"Master, Zugriff auf das Video-Wiedergabesystem für {suche} wird initialisiert.")
    pywhatkit.playonyt(suche)


def befehl_ausfuehren(befehl):
    """Führt einen Befehl aus. Gibt False zurück, wenn Jarvis deaktiviert werden soll."""
    befehl = ohne_wake_word(befehl.lower())
    if not befehl:
        sprechen("Master, Kernsubroutinen erfolgreich geladen. Warte auf weitere Anweisungen.")
        return True

    if "standby" in befehl:
        sprechen("Bestätigt, Master. Standby-Modus aktiviert. Systeme in Bereitschaft.")
        return False

    if execute_command(befehl, sprechen):
            return True

    try:
            set_voice_state("thinking", "Systemanalyse läuft")
            antwort = frage_ki(befehl)
            sprechen(antwort)

    except Exception as error:
            log(error)
            sprechen("Master, kritischer Systemfehler. Kommunikationssystem offline. Zugriff auf Kernsysteme nicht möglich.")
    return True

def main():
    starte_ui()
    threading.Thread(target=supervisor_watchdog, daemon=True).start()
    aktiv = False
    set_voice_state("idle", "Standby-Protokoll aktiv. Aktivierung über das Schlüsselwort 'Jarvis")

    while True:
        if not aktiv:
            # Im Standby wird alles ignoriert, was nicht das Wake-Word enthält.
            set_voice_state("idle", "Standby-Protokoll aktiv. Aktivierung über das Schlüsselwort 'Jarvis")
            gehoert = zuhoeren(wake_only=True)
            if "jarvis" not in gehoert.lower():
                continue

            aktiv = True
            direkter_befehl = ohne_wake_word(gehoert)
            if direkter_befehl:
                if not befehl_ausfuehren(direkter_befehl):
                    aktiv = False
            else:
                sprechen("Bestätigt, Master. Systemstatus optimal, ich stehe bereit, weitere Befehle entgegenzunehmen.")
            continue

        befehl = zuhoeren()
        if not befehl:
            continue
        if not befehl_ausfuehren(befehl):
            aktiv = False
            set_voice_state("idle", "Standby-Protokoll aktiv. Aktivierung über das Schlüsselwort 'Jarvis")


if __name__ == "__main__":
    main()
