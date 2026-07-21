import os
import psutil
import webbrowser
import time
import pyautogui
import pyperclip
from pathlib import Path
import pywhatkit

# Programme werden einmal eingelesen
PROGRAMME = {}

# Bekannte Aliasse
ALIASE = {
    "ls25": "farming simulator 25",
    "fs25": "farming simulator 25",
    "epic": "epic games launcher",
    "epic games": "epic games launcher",
    "battlenet": "battle.net",
    "battle net": "battle.net",
    "steam": "steam",
    "discord": "discord",
    "infinity": "tikfinity",
    "tic infinity": "tikfinity",
    "finn": "tikfinity",
    "tic finity": "tikfinity",
    "joystick gremlin": "joystick_gremlin",
    "joystick ram": "joystick_gremlin",
    "": "joystick_gremlin",
    "joystick grimm": "joystick_gremlin",
    "joystick grem": "joystick_gremlin",
    "": "joystick_gremlin",
    "joystick rim": "joystick_gremlin",
}

def programme_scannen():
    """Liest Programme aus dem Windows-Startmenü und allen Laufwerken ein."""

    global PROGRAMME

    if PROGRAMME:
        return

    # Startmenü
    startmenu = [
        Path(os.environ["ProgramData"]) / "Microsoft/Windows/Start Menu/Programs",
        Path(os.environ["APPDATA"]) / "Microsoft/Windows/Start Menu/Programs",
    ]

    for ordner in startmenu:

        if not ordner.exists():
            continue

        for datei in ordner.rglob("*.lnk"):

            name = datei.stem.lower().strip()

            if name not in PROGRAMME:
                PROGRAMME[name] = {
                    "name": name,
                    "path": str(datei),
                }

    # Ganze Laufwerke nach EXE-Dateien durchsuchen
    laufwerke = [
        "C:\\",
        "E:\\",
        "F:\\",
    ]

    for laufwerk in laufwerke:

        if not os.path.exists(laufwerk):
            continue

        for root, dirs, files in os.walk(laufwerk):

            # Ordner überspringen, die unnötig sind
            dirs[:] = [
                d for d in dirs
                if d.lower() not in (
                    "$recycle.bin",
                    "system volume information",
                    "windows.old",
                )
            ]

            for datei in files:

                if not datei.lower().endswith(".exe"):
                    continue

                name = Path(datei).stem.lower().replace("_", " ").strip()

                if name not in PROGRAMME:
                    PROGRAMME[name] = {
                        "name": name,
                        "path": str(Path(root) / datei),
                    }

    print(f"{len(PROGRAMME)} Programme gefunden.")


def list_programs():
    """Gibt alle Programmnamen zurück."""

    programme_scannen()

    return sorted(PROGRAMME.keys())


def get_programs():
    """Gibt alle Programme mit Informationen zurück."""

    programme_scannen()

    return PROGRAMME

def open_program(programm):
    """Öffnet Programme und Spiele."""

    programme_scannen()

    programm = programm.lower().strip()
    programm = ALIASE.get(programm, programm)

    if programm in PROGRAMME:
        os.startfile(PROGRAMME[programm]["path"])
        return True

    for name, daten in PROGRAMME.items():
        if programm in name:
            os.startfile(daten["path"])
            return True

    return False

def close_program(programm):
    """Beendet ein laufendes Programm."""

    programme_scannen()

    programm = programm.lower().strip()
    programm = ALIASE.get(programm, programm)

    PROZESS_ALIASE = {
        "spotify": ["spotify"],
        "discord": ["discord"],
        "steam": ["steam"],
        "epic games launcher": ["epicgameslauncher"],
        "battle.net": ["battle.net", "agent"],
        "google chrome": ["chrome"],
        "chrome": ["chrome"],
        "firefox": ["firefox"],
        "opera": ["opera"],
        "microsoft edge": ["msedge"],
        "edge": ["msedge"],
        "farming simulator 25": ["farmingimulator2025game"],
        "tikfinity": ["tikfinity"],
        "joystick_gremlin": ["joystick_gremlin.exe"],
    }

    suchbegriffe = PROZESS_ALIASE.get(programm, [programm])

    gefunden = False

    for prozess in psutil.process_iter(["pid", "name"]):
        try:
            name = (prozess.info["name"] or "").lower()

            for begriff in suchbegriffe:
                if begriff in name:

                    try:
                        prozess.terminate()
                        prozess.wait(timeout=3)
                    except psutil.TimeoutExpired:
                        prozess.kill()

                    gefunden = True
                    break

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):
            pass

    return gefunden


def open_folder(ordner):
    """Öffnet bekannte Windows-Ordner."""

    home = Path.home()

    ordner_liste = {
        "downloads": home / "Downloads",
        "dokumente": home / "Documents",
        "bilder": home / "Pictures",
        "musik": home / "Music",
        "videos": home / "Videos",
        "desktop": home / "Desktop",
    }

    ordner = ordner.lower().strip()

    if ordner in ordner_liste:
        os.startfile(ordner_liste[ordner])
        return True

    return False


def open_website(url):
    """Öffnet Webseiten."""

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    webbrowser.open(url)
    return True

def play_youtube(suche):

    pywhatkit.playonyt(suche)

    return True

def spotify_play(song):
    """Öffnet Spotify, sucht einen Titel und startet ihn."""

    # Spotify öffnen
    open_program("spotify")
    time.sleep(4)

    # Suche öffnen
    pyautogui.hotkey("ctrl", "l")
    time.sleep(0.3)

    pyautogui.hotkey("ctrl", "k")
    time.sleep(0.3)

    # Suchfeld leeren
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("backspace")

    # Titel eingeben
    pyperclip.copy(song)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1)

    # Suche ausführen
    pyautogui.press("enter")
    time.sleep(1.5)

    # Ersten Treffer starten
    #pyautogui.moveTo(576, 438, duration=0.3)
    #pyautogui.click()

    return True

def spotify_pause():
    pyautogui.press("space")
    return True


def spotify_next():
    pyautogui.hotkey("ctrl", "right")
    return True


def spotify_previous():
    pyautogui.hotkey("ctrl", "left")
    return True


def volume_up():
    pyautogui.hotkey("ctrl", "up")
    return True


def volume_down():
    pyautogui.hotkey("ctrl", "down")
    return True


def volume_mute():
    pyautogui.press("volumemute")
    return True