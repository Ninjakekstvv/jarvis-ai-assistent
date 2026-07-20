import datetime
from ipc import send_command
from actions import (
    open_program,
    open_website,
    play_youtube,
    close_program,
    spotify_pause,
    spotify_next,
    spotify_previous,
    volume_up,
    volume_down,
    volume_mute,
    spotify_play,
)


WEBSEITEN = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.de",
    "amazon": "https://www.amazon.de",
    "chatgpt": "https://chatgpt.com",
    "github": "https://github.com",
    "tiktok": "https://www.tiktok.com",
}

def execute_command(befehl, sprechen):

    befehl = befehl.lower().strip()

    # ==========================
    # Begrüßung
    # ==========================

    if befehl == "hallo":
        sprechen("Hallo, Master. Keine kritischen Systemfehler erkannt. Alle Systeme arbeiten innerhalb der optimalen Parameter.")
        return True

    if "wie geht" in befehl:
        sprechen("Ausgezeichnet, Master. Alle Systeme arbeiten innerhalb der optimalen Parameter. Meine Diagnoseroutinen empfehlen dennoch gelegentlich eine Wartung, rein vorsorglich.")
        return True

    # ==========================
    # Programme anzeigen
    # ==========================

    if "programmliste" in befehl or "programm liste" in befehl:

        if "schließ" in befehl or "schliesse" in befehl or "schließen" in befehl:
            if send_command("CLOSE_PROGRAMS"):
                sprechen("Master, Abschaltungsprotokoll der Systemmodule wird initialisiert.")
            else:
                sprechen("Master, Abschaltungsprotokoll der Systemmodule konnte nicht abgeschlossen werden.")
            return True

        if "öffne" in befehl or "zeige" in befehl:
            if send_command("SHOW_PROGRAMS"):
                sprechen("Master, Zugriff auf Systemmodule wird initialisiert.")
            else:
                sprechen("Master Systemmodule reagieren nicht wie erwartet. Initialisierung abgebrochen.")
            return True

    # ==========================
    # YouTube Musik
    # ==========================

    if befehl.startswith("spotify spiele "):

        titel = befehl.replace("spotify spiele ", "").strip()

        sprechen(f"Zugriff auf das Wiedergabesystem Für {titel} wird initialisiert Master.")

        spotify_play(titel)

        return True

    if befehl.startswith(("spiele ", "spiel ")):

        suche = (
            befehl.replace("spiele ", "")
                  .replace("spiel ", "")
                  .strip()
        )

        if open_program("spotify"):

           sprechen(f"Master, Initialisierung des Wiedergabesystems für {suche} Wurde Erfolgreich Initialisiert .")
           spotify_play(suche)

        else:

            sprechen(f"Master, Initialisierung des Video-Wiedergabesystem für {suche} Wurde Erfolgreich Initialisiert.")
            play_youtube(suche)

        return True

    # ==========================
    # Öffnen / Starten
    # ==========================

    if befehl.startswith(("öffne ", "starte ")):

        ziel = (
            befehl.replace("öffne ", "")
                  .replace("starte ", "")
                  .strip()
        )

        if ziel in WEBSEITEN:
            open_website(WEBSEITEN[ziel])
            sprechen(f"Master, Zielsystem {ziel} konnte nicht lokalisiert werden.")
            return True

        if open_program(ziel):
            sprechen(f"Master, Zugriff auf Ortungssystem {ziel} wird initialisiert.")
            return True

        sprechen(f"{ziel} Master, Ziel- oder Ortungssystem konnte nicht lokalisiert werden.")
        return True

    # ==========================
    # Programme schließen
    # ==========================

    if befehl.startswith(("schließe ", "schliesse ", "beende ")):

        ziel = (
            befehl.replace("schließe ", "")
                  .replace("schliesse ", "")
                  .replace("beende ", "")
                  .strip()
        )

        if close_program(ziel):
            sprechen(f"{ziel} Abschaltungsprotokoll erfolgreich abgeschlossen Master.")
        else:
            sprechen(f"Abschaltungsprotokoll für Zielsystem {ziel} fehlgeschlagen.")

        return True

    # ==========================
    # Spotify / Mediensteuerung
    # ==========================

    if befehl in (
        "pause",
        "musik pausieren",
        "spotify pausieren",
        "weiter",
        "musik weiter",
        "spotify weiter",
    ):
        spotify_pause()
        sprechen("Master, Wiedergabeprotokoll angehalten.")
        return True

    if befehl in (
        "nächstes lied",
        "weiteres lied",
        "spotify nächstes lied",
    ):
        spotify_next()
        sprechen("Wiedergabeprotokoll auf den nächsten Eintrag umgestellt.")
        return True

    if befehl in (
        "vorheriges lied",
        "letztes lied",
        "spotify vorheriges lied",
    ):
        spotify_previous()
        sprechen("Master, Wiedergabeprotokoll auf den vorherigen Eintrag zurückgesetzt.")
        return True

    if befehl in (
        "lauter",
        "musik lauter",
    ):
        volume_up()
        sprechen("lauter: Master, Verstärkungsmodul neu kalibriert.")
        return True

    if befehl in (
        "leiser",
        "musik leiser",
    ):
        volume_down()
        sprechen("Master, Verstärkungsmodul auf Minimalbetrieb gesetzt.")
        return True

    if befehl in (
        "ton aus",
        "stumm",
    ):
        volume_mute()
        sprechen("Master, Akustiksubsystem in den Ruhezustand versetzt.")
        return True

    # ==========================
    # Uhrzeit
    # ==========================

    if befehl == "uhrzeit":
        zeit = datetime.datetime.now().strftime("%H:%M")
        sprechen(f"Master, Chronometersystem synchronisiert. Aktuelle Systemzeit: {zeit} Alle zeitkritischen Routinen arbeiten innerhalb der optimalen Parameter.")
        return True

    return False