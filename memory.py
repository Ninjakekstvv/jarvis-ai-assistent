import sqlite3
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "memory.db")


def verbindung():
    return sqlite3.connect(DB_NAME)



def init_memory():
    """Erstellt die Datenbank beim ersten Start."""

    conn = verbindung()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()



def merken(key, value):
    """Speichert oder aktualisiert eine Erinnerung."""

    conn = verbindung()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO memory (key, value)
        VALUES (?, ?)
    """, (key, value))

    conn.commit()
    conn.close()



def erinnern(key):
    """Liest eine Erinnerung."""

    conn = verbindung()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT value FROM memory WHERE key = ?",
        (key,)
    )

    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]

    return None



def vergessen(key):
    """Löscht eine Erinnerung."""

    conn = verbindung()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM memory WHERE key = ?",
        (key,)
    )

    conn.commit()
    conn.close()



def alles_wissen():
    """Gibt alle gespeicherten Erinnerungen zurück."""

    conn = verbindung()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT key, value FROM memory"
    )

    daten = cursor.fetchall()

    conn.close()

    return daten



def memory_status():
    """Zeigt Anzahl gespeicherter Erinnerungen."""

    conn = verbindung()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM memory"
    )

    anzahl = cursor.fetchone()[0]

    conn.close()

    return anzahl



# Datenbank automatisch vorbereiten
init_memory()