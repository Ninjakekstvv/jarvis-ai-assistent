from memory import merken, erinnern, vergessen, alles_wissen



KATEGORIEN = {

    # Benutzer
    "name": "user_name",
    "master_name": "user_name",
    "benutzername": "user_name",
    "username": "user_name",


    # Projekte
    "projekt": "project_current",
    "projekte": "project_current",
    "aktuelles_projekt": "project_current",

    "fokus": "project_focus",
    "projekt_fokus": "project_focus",
    "aktueller_fokus": "project_focus",

    "status": "project_status",
    "projektstatus": "project_status",
    "current_work_focus": "project_focus",
    
    "arbeitsfokus": "project_focus",
    "arbeits_fokus": "project_focus",
    "aktueller_arbeitsfokus": "project_focus",

    "arbeit_am": "project_focus",
    "arbeite_an": "project_focus",


    # Hardware
    "hardware.grafikkarte": "hardware_gpu",
    "grafikkarte": "hardware_gpu",
    "gpu": "hardware_gpu",

    "hardware.prozessor": "hardware_cpu",
    "prozessor": "hardware_cpu",
    "cpu": "hardware_cpu",


    # Einstellungen
    "sprache": "user_language",
    "stil": "user_style",
}



def normalisiere(key):

    if not key:
        return ""


    key = key.lower().strip()


    if key in KATEGORIEN:
        return KATEGORIEN[key]


    key = key.replace(" ", "_")


    return KATEGORIEN.get(
        key,
        key
    )



def speichern(key, value):

    sauber = normalisiere(key)


    if sauber and value:

        merken(
            sauber,
            value
        )

        return True


    return False



def abrufen(key):

    return erinnern(
        normalisiere(key)
    )



def entfernen(key):

    vergessen(
        normalisiere(key)
    )



def profil():

    daten = alles_wissen()

    result = {}


    for key, value in daten:

        result[key] = value


    return result



def kontext():

    daten = profil()


    text = ""


    if "project_current" in daten:

        text += (
            f"Aktuelles Projekt: "
            f"{daten['project_current']}\n"
        )


    if "project_focus" in daten:

        text += (
            f"Aktueller Fokus: "
            f"{daten['project_focus']}\n"
        )


    if "project_status" in daten:

        text += (
            f"Projektstatus: "
            f"{daten['project_status']}\n"
        )


    return text



def status():

    return {

        "gespeicherte_eintraege":
            len(profil()),

        "kontext":
            kontext(),

        "aktiv":
            True
    }