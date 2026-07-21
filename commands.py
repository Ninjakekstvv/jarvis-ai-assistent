import datetime
import traceback
import threading
import sys
import os

from ipc import send_command
from builder.project_builder import ProjectBuilder

from tasks import aufgabe_erstellen

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



builder = ProjectBuilder()



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

        sprechen(
            "Hallo, Master. Alle Systeme arbeiten innerhalb der optimalen Parameter."
        )

        return True



    if "wie geht" in befehl:

        sprechen(
            "Ausgezeichnet, Master. Systemstatus optimal."
        )

        return True



    # ==========================
    # Jarvis beenden
    # ==========================

    if befehl in (

        "jarvis beenden",
        "jarvis ausschalten",
        "jarvis herunterfahren",
        "jarvis aus",
        "beende jarvis",
        "shutdown",

    ):

        sprechen(
            "Master. Abschaltungsprotokoll wird initialisiert."
        )

        os._exit(0)



    # ==========================
    # AUFGABEN MODUL
    # ==========================

    task_trigger = (

        "erstelle eine aufgabe ",
        "erstelle aufgabe ",
        "füge eine aufgabe hinzu ",
        "merke dir als aufgabe ",
        "neue aufgabe ",

    )


    if befehl.startswith(task_trigger):


        prefix = next(
            t for t in task_trigger
            if befehl.startswith(t)
        )


        task = befehl.replace(
            prefix,
            ""
        ).strip()



        if not task:

            sprechen(
                "Master, welche Aufgabe soll registriert werden?"
            )

            return True



        aufgabe_erstellen(
            task
        )


        sprechen(
            f"Aufgabe registriert, Master. {task} wurde im Aufgabenmodul gespeichert."
        )


        return True




    # ==========================
    # PROJEKTE ERSTELLEN
    # ==========================


    trigger = (

        "programmiere ",
        "entwickle ",
        "baue ",
        "schreibe ",
        "generiere ",

    )


    if befehl.startswith(trigger):


        prefix = next(
            t for t in trigger
            if befehl.startswith(t)
        )


        task = befehl.replace(
            prefix,
            ""
        ).strip()



        if not task:

            sprechen(
                "Master, was soll entwickelt werden?"
            )

            return True



        sprechen(
            "Master, Projektanalyse gestartet."
        )


        try:


            result = builder.build(
                task
            )


            sprechen(
                "Master, Projekt wurde erfolgreich erstellt."
            )


            print(result)



        except Exception as e:


            print(e)


            sprechen(
                "Master, Projekterstellung fehlgeschlagen."
            )



        return True




    # ==========================
    # PROGRAMME ANZEIGEN
    # ==========================


    if "programmliste" in befehl or "programm liste" in befehl:


        if "schließ" in befehl:

            send_command(
                "CLOSE_PROGRAMS"
            )

            sprechen(
                "Systemmodule werden geschlossen, Master."
            )

            return True



        if "öffne" in befehl:

            send_command(
                "SHOW_PROGRAMS"
            )

            sprechen(
                "Systemmodule werden angezeigt, Master."
            )

            return True





    # ==========================
    # YOUTUBE
    # ==========================


    if befehl.startswith(
        (
            "spiele ",
            "spiel "
        )
    ):


        suche = (

            befehl
            .replace("spiele ", "")
            .replace("spiel ", "")
            .strip()

        )


        play_youtube(
            suche
        )


        sprechen(
            "Wiedergabesystem aktiviert, Master."
        )


        return True




    # ==========================
    # ÖFFNEN
    # ==========================


    if befehl.startswith(
        (
            "öffne ",
            "starte "
        )
    ):


        ziel = (

            befehl
            .replace("öffne ", "")
            .replace("starte ", "")
            .strip()
            .replace(" ","")

        )


        if ziel in WEBSEITEN:


            open_website(
                WEBSEITEN[ziel]
            )


            sprechen(
                f"{ziel} wurde geöffnet, Master."
            )


            return True



        if open_program(ziel):


            sprechen(
                f"{ziel} gestartet, Master."
            )


            return True



    # ==========================
    # SCHLIESSEN
    # ==========================


    if befehl.startswith(
        (
            "schließe ",
            "schliesse ",
            "beende "
        )
    ):


        ziel = (

            befehl
            .replace("schließe ","")
            .replace("schliesse ","")
            .replace("beende ","")
            .strip()

        )


        close_program(
            ziel
        )


        sprechen(
            f"{ziel} Abschaltungsprotokoll abgeschlossen."
        )


        return True





    # ==========================
    # MEDIEN
    # ==========================


    if befehl in (

        "pause",
        "musik pausieren",
        "spotify pausieren",

    ):


        spotify_pause()

        sprechen(
            "Wiedergabe pausiert, Master."
        )

        return True



    if befehl in (

        "nächstes lied",
        "weiteres lied",

    ):


        spotify_next()

        sprechen(
            "Nächster Titel aktiviert."
        )

        return True




    # ==========================
    # UHRZEIT
    # ==========================


    if befehl == "uhrzeit":


        zeit = datetime.datetime.now().strftime(
            "%H:%M"
        )


        sprechen(
            f"Master, aktuelle Systemzeit {zeit}."
        )


        return True



    return False