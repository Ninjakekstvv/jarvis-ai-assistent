import json
import re
from openai import OpenAI

from memory_manager import speichern, abrufen, entfernen, profil

from tasks import (
    aufgabe_erstellen,
    aufgaben_anzeigen,
    aufgabe_erledigt,
    aufgabe_loeschen,
    prioritaet_aendern,
    aufgabe_zuweisen,
)


client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio"
)


MODEL = "qwen3.5-9b"



def normalisiere_key(key):

    if not key:
        return ""


    mapping = {

        "master_name": "user_name",
        "master": "user_name",
        "name": "user_name",
        "username": "user_name",
        "benutzername": "user_name",

        "projekt": "project_current",
        "projekte": "project_current",
        "aktuelles_projekt": "project_current",

        "current_work_focus": "project_focus",
        "work_focus": "project_focus",
        "arbeitsfokus": "project_focus",
        "aktueller_fokus": "project_focus",
        "aktueller_arbeitsfokus": "project_focus",

        "current_status": "project_status",
        "projektstatus": "project_status",

        "hardware.grafikkarte": "hardware_gpu",
        "grafikkarte": "hardware_gpu",
        "gpu": "hardware_gpu",

        "hardware.prozessor": "hardware_cpu",
        "prozessor": "hardware_cpu",
        "cpu": "hardware_cpu",

    }


    key = key.lower().strip()


    return mapping.get(
        key,
        key.replace(" ", "_")
    )



SYSTEM_PROMPT = """
Du bist Jarvis, ein hochentwickelter KI-Assistent.

Sprich den Benutzer immer mit Master an.

Antworte kurz, präzise und analytisch.

Verwende Systembegriffe:
- Systemstatus
- Kernsysteme
- Diagnose
- Bereitschaft
- Parameter


Langzeitgedächtnis:

Speichere:
- Name
- Projekte
- Hardware
- Vorlieben
- Einstellungen
- Arbeitsfokus


Aufgabenverwaltung:

task_add:

{
 "tool":"task_add",
 "parameters":{
    "task":"..."
 }
}


task_list:

{
 "tool":"task_list",
 "parameters":{}
}


task_done:

{
 "tool":"task_done",
 "parameters":{
    "id":1
 }
}


task_delete:

{
 "tool":"task_delete",
 "parameters":{
    "id":1
 }
}

task_priority:

{
 "tool":"task_priority",
 "parameters":{
    "id":1,
    "priority":"hoch"
 }
}

task_assign:

{
 "tool":"task_assign",
 "parameters":{
    "id":1,
    "person":"Master"
 }
}


Wichtig bei Prioritäten:

task_priority verändert immer eine bereits vorhandene Aufgabe.

Wenn der Master sagt:
- "Setze Aufgabe 1 auf Priorität hoch"
- "Ändere die Priorität von Aufgabe 2"
- "Aufgabe 3 wichtig machen"

Dann immer:
task_priority verwenden.

Keine neue Aufgabe erstellen.

task_add nur benutzen, wenn der Master ausdrücklich eine neue Aufgabe erstellen möchte.

Bei Werkzeugen:
Nur gültiges JSON.
Kein Markdown.
"""



def _frage_llm(messages):

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.6,
        messages=messages
    )

    return response.choices[0].message.content



def lade_memory():

    daten = profil()

    if not daten:
        return ""


    text = "\n\nLangzeitgedächtnis des Masters:\n"


    for key,value in daten.items():

        text += f"- {key}: {value}\n"


    return text



def antwort_an_user(text):

    return _frage_llm(
        [
            {
                "role":"system",
                "content":
                SYSTEM_PROMPT + lade_memory()
            },

            {
                "role":"user",
                "content":text
            }
        ]
    )



def bereinige_json(text):

    text = text.strip()

    text = re.sub(
        r"```json",
        "",
        text,
        flags=re.I
    )

    text = text.replace(
        "```",
        ""
    )

    return text.strip()



def frage_ki(frage):

    antwort = antwort_an_user(frage)


    try:

        tool = json.loads(
            bereinige_json(antwort)
        )

    except Exception:

        return antwort



    name = tool.get("tool")

    params = tool.get(
        "parameters",
        {}
    )



    if name == "remember":

        key = normalisiere_key(
            params.get("key")
        )

        value = params.get("value")

        speichern(
            key,
            value
        )

        return antwort_an_user(
            f"Information gespeichert: {key} = {value}"
        )



    elif name == "recall":

        key = normalisiere_key(
            params.get("key")
        )

        wert = abrufen(
            key
        )

        return antwort_an_user(
            f"Gespeicherter Wert: {key} = {wert}"
        )



    elif name == "forget":

        key = normalisiere_key(
            params.get("key")
        )

        entfernen(
            key
        )

        return antwort_an_user(
            f"Information entfernt: {key}"
        )



    elif name == "task_add":

        task = params.get(
            "task"
        )

        aufgabe_erstellen(
            task
        )

        return antwort_an_user(
            f"Aufgabe registriert: {task}"
        )



    elif name == "task_list":

        daten = aufgaben_anzeigen()


        if not daten:

            return "Systemstatus: Keine Aufgaben gespeichert, Master."


        liste = "Aktuelle Aufgaben:\n\n"


        for aufgabe in daten:

            liste += (
                f"Aufgabe: {aufgabe[0]}\n"
                f"Titel: {aufgabe[1]}\n"
                f"Status: {aufgabe[2]}\n"
                f"Priorität: {aufgabe[3]}\n\n"
            )


        return liste



    elif name == "task_done":

        task_id = params.get(
            "id"
        )

        aufgabe_erledigt(
            task_id
        )

        return antwort_an_user(
            f"Aufgabe {task_id} erledigt."
        )



    elif name == "task_delete":

        task_id = params.get(
            "id"
        )


        erfolgreich = aufgabe_loeschen(
            task_id
        )


        if erfolgreich:

            return (
                f"Systemstatus: Aufgabe {task_id} "
                "wurde gelöscht, Master."
            )

        else:

            return (
                f"Systemstatus: Aufgabe {task_id} "
                "konnte nicht gefunden werden, Master."
            )



    elif name == "task_priority":

        task_id = params.get(
            "id"
        )

        priority = params.get(
            "priority"
        )


        erfolgreich = prioritaet_aendern(
            task_id,
            priority
        )


        if erfolgreich:

            return (
                f"Systemstatus: Priorität von Aufgabe "
                f"{task_id} auf {priority} gesetzt, Master."
            )

        else:

            return (
                f"Systemstatus: Aufgabe {task_id} nicht gefunden."
            )



    elif name == "task_assign":

        task_id = params.get(
            "id"
        )

        person = params.get(
            "person"
        )


        erfolgreich = aufgabe_zuweisen(
            task_id,
            person
        )


        if erfolgreich:

            return (
                f"Systemstatus: Aufgabe {task_id} "
                f"wurde {person} zugewiesen, Master."
            )

        else:

            return (
                f"Systemstatus: Aufgabe {task_id} nicht gefunden."
            )


    return antwort